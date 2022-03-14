import os
import typing as t
import asyncio
import discord
from discord.ext import commands
import random

from roll import Roll
from table import Table
from character import Character, Attribute, ActiveSkill, LINKED_ATTRIBUTE
from database import save_character, load_character

bot = commands.Bot(command_prefix='-', activity=discord.Game(name='Shadowrun 5e'))


@bot.event
async def on_ready():
    print('Bot Ready!')


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


def get_roll_description(result):
    desc = ""
    for i in range(0, len(result.results)):
        if result.results[i] >= 5:
            desc += f"**{result.results[i]}**"
        else:
            desc += str(result.results[i])

        if i != len(result.results) - 1:
            desc += ", "

    if desc != "":
        desc += "\n"
    desc += f"**{result.hits} hits**"

    if result.critical_glitch:
        desc += "\n**Critical Glitch!**"
    elif result.glitch:
        desc += "\n**Glitch!**"

    return desc


@bot.command(aliases=["r"])
async def roll(ctx, numb: int):
    result = Roll.roll(numb)

    desc = get_roll_description(result)

    char = load_character(ctx.guild.id, ctx.author.id)
    name = ctx.author.display_name if char is None else char.name

    msg_embed = discord.Embed(title=f"{name} rolls {numb}d6!",
                              description=desc,
                              color=char.settings.color or random.randint(0, 0xffffff))

    await ctx.message.delete()
    await ctx.send(embed=msg_embed)


async def send_table(channel: discord.abc.Messageable, tb: Table):
    await channel.send(
        f"**{tb.name} Table** ({tb.book} pg. {tb.page})",
        file=discord.File(tb.path)
    )


@bot.command()
async def table(ctx, *args):
    query = " ".join(args)
    results = Table.lookup_table(query)
    if len(results) == 1:
        await send_table(ctx.channel, results[0])
        return

    options = {}
    desc = "Which one are you looking for? (Type the number or \"c\" to cancel)"
    for i in range(0, len(results)):
        options[str(i + 1)] = results[i]
        desc += f"\n**[{i + 1}]** {results[i].name} ({results[i].book})"

    msg_embed = discord.Embed(title=f"Multiple Matches Found for \"{query}\"",
                              description=desc,
                              color=random.randint(0, 0xffffff))

    selection_msg = await ctx.send(embed=msg_embed)

    try:
        reply = await bot.wait_for("message",
                                   check=lambda m: m.channel == ctx.channel and m.author == ctx.author and
                                                   (m.content in options.keys() or m.content == 'c'),
                                   timeout=30.0)

        if reply.content == 'c':
            await ctx.send("Selection cancelled")
        else:
            await send_table(ctx.channel, options[reply.content])
        await reply.delete()

    except asyncio.TimeoutError:
        await ctx.send("Selection timed out")

    await selection_msg.delete()


@bot.command()
async def gsheet(ctx, url: str):
    try:
        char = Character.from_url(url, ctx.guild.id, ctx.author.id)
    except ValueError as e:
        await ctx.send(str(e))
        return
    except Exception as e:
        print(repr(e))
        await ctx.send("Failed to load character")
        return

    save_character(char)
    await ctx.send(f"Loaded character \"{char.name}\"")


@bot.command()
async def update(ctx):
    char = load_character(ctx.guild.id, ctx.author.id)
    if char is None:
        await ctx.send("You have no linked sheet on this server. Use -gsheet to link one.")
        return
    try:
        char.update()
    except ValueError as e:
        await ctx.send(str(e))
    except Exception as e:
        print(repr(e))
        await ctx.send("Failed to load character")
    else:
        await ctx.send(f"Loaded character \"{char.name}\"")


@bot.command(aliases=["c"])
async def check(ctx, *args):
    # TODO: Limits
    char = load_character(ctx.guild.id, ctx.author.id)
    if char is None:
        await ctx.send("You have no linked sheet on this server. Use -gsheet to link one.")
        return

    clean_args = []
    for arg in args:
        for split_arg in arg.split('+'):
            split_arg.replace(" ", "_")
            split_arg = split_arg.upper()
            clean_args.append(split_arg)

    pool_builders = []
    roll_name = ""
    i = -1
    while i < len(clean_args) - 1:
        i += 1
        roll_name += " "
        arg = clean_args[i]
        if arg == "COMPOSURE":
            pool_builders.append(Attribute.CHARISMA)
            pool_builders.append(Attribute.WILLPOWER)
            roll_name += "Composure"
            continue
        if arg == "JUDGE_INTENTIONS":
            pool_builders.append(Attribute.CHARISMA)
            pool_builders.append(Attribute.INTUITION)
            roll_name += "Judge Intentions"
            continue
        if arg == "JUDGE" and i + 1 < len(clean_args) and clean_args[i + 1] == "INTENTIONS":
            i += 1
            pool_builders.append(Attribute.CHARISMA)
            pool_builders.append(Attribute.INTUITION)
            roll_name += "Judge Intentions"
            continue
        if arg in ("LIFT", "LIFTING") and i + 1 < len(clean_args) and clean_args[i + 1] in ("CARRY", "CARRYING"):
            i += 1
            pool_builders.append(Attribute.BODY)
            pool_builders.append(Attribute.STRENGTH)
            roll_name += "Lift/Carry"
            continue
        if arg in ("LIFT", "CARRY", "LIFT/CARRY", "LIFT_CARRY",
                   "LIFTING" "CARRYING" "LIFTING/CARRYING", "LIFTING_CARRYING"):
            pool_builders.append(Attribute.BODY)
            pool_builders.append(Attribute.STRENGTH)
            roll_name += "Lift/Carry"
            continue
        if arg == "MEMORY":
            pool_builders.append(Attribute.LOGIC)
            pool_builders.append(Attribute.WILLPOWER)
            roll_name += "Memory"
            continue
        if arg == "SURPRISE":
            pool_builders.append(Attribute.REACTION)
            pool_builders.append(Attribute.INTUITION)
            roll_name += "Surprise"
            continue
        if arg == "DODGE":
            pool_builders.append(Attribute.REACTION)
            pool_builders.append(Attribute.INTUITION)
            roll_name += "Dodge"
            continue

        skill = None
        try:
            skill = ActiveSkill[arg]
        except KeyError:
            if i + 1 < len(clean_args):
                try:
                    skill = ActiveSkill[arg + "_" + clean_args[i + 1]]
                    i += 1
                except KeyError:
                    pass
        if skill is not None:
            pool_builders.append(skill)
            name = skill.name.lower()
            name = " ".join([w[0].upper() + w[1:] for w in name.split("_")])
            roll_name += name
            continue

        attr = None
        try:
            attr = Attribute[arg]
        except KeyError:
            for a in list(Attribute):
                if arg == a.value:
                    attr = a
                    break
        if attr is not None:
            pool_builders.append(attr)
            roll_name += attr.name[0] + attr.name[1:].lower()
            continue

        try:
            modifier = int(arg)
            pool_builders.append(modifier)
        except ValueError:
            await ctx.send(f"Could not parse parameter: {arg.lower()}")
            return

    if len([b for b in pool_builders if type(b) == ActiveSkill]) == 1 and \
            len([b for b in pool_builders if type(b) == Attribute]) == 0:
        skill = None
        for b in pool_builders:
            if type(b) == ActiveSkill:
                skill = b
                break
        pool_builders.append(LINKED_ATTRIBUTE[skill])

    if char.settings.do_defaulting and len([b for b in pool_builders if type(b) == ActiveSkill]) == 1 and \
            len([b for b in pool_builders if type(b) == Attribute]) == 1:
        for b in pool_builders:
            if type(b) == ActiveSkill:
                if char.skills[b] == 0:
                    pool_builders.append("Defaulting")
                break

    if len([b for b in pool_builders if type(b) != int]) == 0:
        await ctx.send("The check command needs at least one non-modifier argument")
        return

    pool_builders.sort(key=lambda b: (type(b) == ActiveSkill) +
                                     (type(b) == Attribute) * 2 +
                                     (type(b) == str) * 3 +
                                     (type(b) == int) * 4)

    roll_name = roll_name[1:]
    if roll_name.endswith(" "):
        roll_name = roll_name[:-1]

    pool = 0
    pool_desc = ""
    for builder in pool_builders:
        if type(builder) == Attribute:
            dice = char.attributes[builder]
            name = builder.name[0] + builder.name[1:].lower()
            if pool_desc != "":
                pool_desc += "+ "
            pool_desc += f"{name}({dice})"
            pool += dice
        elif type(builder) == ActiveSkill:
            dice = char.skills[builder]
            if dice == 0:
                continue
            name = " ".join([w[0] + w[1:].lower() for w in builder.name.split("_")])
            if pool_desc != "":
                pool_desc += "+ "
            pool_desc += f"{name}({dice})"
            pool += dice
        elif type(builder) == str:
            if builder == "Defaulting":
                pool -= 1
                pool_desc += "+ Defaulting(-1)"
        elif type(builder == int):
            if builder >= 0:
                pool_desc += f"+ {builder}"
            else:
                pool_desc += f"- {-builder}"
            pool += builder
        else:
            raise ValueError(f"Illegal pool builder type: {builder}")
        pool_desc += " "

    pool = max(0, pool)
    pool_desc += f"= {pool}"

    result = Roll.roll(pool)
    desc = pool_desc + "\n" + get_roll_description(result)

    title = f"{char.name} makes " \
            f"{'an' if len(roll_name) > 0 and roll_name[0].upper() in ('A', 'E', 'I', 'O', 'U') else 'a'} " \
            f"{roll_name} check!"
    msg_embed = discord.Embed(title=title,
                              description=desc,
                              color=char.settings.color or random.randint(0, 0xffffff))

    await ctx.message.delete()
    await ctx.send(embed=msg_embed)


if __name__ == "__main__":
    bot.run(os.getenv("token"))
