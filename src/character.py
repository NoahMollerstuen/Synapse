import math
import typing as t
import enum
from enum import Enum
from gsheets import Sheets

sheets = Sheets.from_files('resources/sheets/client_secrets.json', 'resources/sheets/storage.json')


class Attribute(Enum):
    BODY = "BOD"
    AGILITY = "AGI"
    REACTION = "REA"
    STRENGTH = "STR"
    WILLPOWER = "WIL"
    LOGIC = "LOG"
    INTUITION = "INT"
    CHARISMA = "CHA"
    MAGIC = "MAG"
    RESONANCE = "RES"
    EDGE = "EDG"
    ESSENCE = "ESS"


class ActiveSkill(Enum):
    ARCHERY = enum.auto()
    AUTOMATICS = enum.auto()
    BLADES = enum.auto()
    CLUBS = enum.auto()
    ESCAPE_ARTIST = enum.auto()
    GUNNERY = enum.auto()
    GYMNASTICS = enum.auto()
    HEAVY_WEAPONS = enum.auto()
    LOCKSMITH = enum.auto()
    LONGARMS = enum.auto()
    PALMING = enum.auto()
    PISTOLS = enum.auto()
    SNEAKING = enum.auto()
    THROWING_WEAPONS = enum.auto()
    UNARMED_COMBAT = enum.auto()
    DIVING = enum.auto()
    FREE_FALL = enum.auto()
    PILOT_AEROSPACE = enum.auto()
    PILOT_AIRCRAFT = enum.auto()
    PILOT_GROUNDCRAFT = enum.auto()
    PILOT_WALKER = enum.auto()
    PILOT_WATERCRAFT = enum.auto()
    RUNNING = enum.auto()
    SWIMMING = enum.auto()
    ANIMAL_HANDLING = enum.auto()
    CON = enum.auto()
    ETIQUETTE = enum.auto()
    IMPERSONATION = enum.auto()
    INSTRUCTION = enum.auto()
    INTIMIDATION = enum.auto()
    LEADERSHIP = enum.auto()
    NEGOTIATION = enum.auto()
    PERFORMANCE = enum.auto()
    ARTISAN = enum.auto()
    ASSENSING = enum.auto()
    DISGUISE = enum.auto()
    NAVIGATION = enum.auto()
    PERCEPTION = enum.auto()
    TRACKING = enum.auto()
    AERONAUTICS_MECHANIC = enum.auto()
    ARCANA = enum.auto()
    ARMORER = enum.auto()
    AUTOMOTIVE_MECHANIC = enum.auto()
    BIOTECHNOLOGY = enum.auto()
    CHEMISTRY = enum.auto()
    COMPUTER = enum.auto()
    CYBERTECHNOLOGY = enum.auto()
    CYBERCOMBAT = enum.auto()
    DEMOLITIONS = enum.auto()
    ELECTRONIC_WARFARE = enum.auto()
    FIRST_AID = enum.auto()
    FORGERY = enum.auto()
    INDUSTRIAL_MECHANIC = enum.auto()
    HACKING = enum.auto()
    HARDWARE = enum.auto()
    MEDICINE = enum.auto()
    NAUTICAL_MECHANIC = enum.auto()
    SOFTWARE = enum.auto()
    ASTRAL_COMBAT = enum.auto()
    SURVIVAL = enum.auto()
    ALCHEMY = enum.auto()
    ARTIFICING = enum.auto()
    BANISHING = enum.auto()
    BINDING = enum.auto()
    COUNTERSPELLING = enum.auto()
    DISENCHANTING = enum.auto()
    RITUAL_SPELLCASTING = enum.auto()
    SPELLCASTING = enum.auto()
    SUMMONING = enum.auto()
    COMPILING = enum.auto()
    DECOMPILING = enum.auto()
    REGISTERING = enum.auto()


LINKED_ATTRIBUTE = {
    ActiveSkill.ARCHERY: Attribute.AGILITY,
    ActiveSkill.AUTOMATICS: Attribute.AGILITY,
    ActiveSkill.BLADES: Attribute.AGILITY,
    ActiveSkill.CLUBS: Attribute.AGILITY,
    ActiveSkill.ESCAPE_ARTIST: Attribute.AGILITY,
    ActiveSkill.GUNNERY: Attribute.AGILITY,
    ActiveSkill.GYMNASTICS: Attribute.AGILITY,
    ActiveSkill.HEAVY_WEAPONS: Attribute.AGILITY,
    ActiveSkill.LOCKSMITH: Attribute.AGILITY,
    ActiveSkill.LONGARMS: Attribute.AGILITY,
    ActiveSkill.PALMING: Attribute.AGILITY,
    ActiveSkill.PISTOLS: Attribute.AGILITY,
    ActiveSkill.SNEAKING: Attribute.AGILITY,
    ActiveSkill.UNARMED_COMBAT: Attribute.AGILITY,
    ActiveSkill.DIVING: Attribute.BODY,
    ActiveSkill.FREE_FALL: Attribute.BODY,
    ActiveSkill.PILOT_AEROSPACE: Attribute.REACTION,
    ActiveSkill.PILOT_AIRCRAFT: Attribute.REACTION,
    ActiveSkill.PILOT_GROUNDCRAFT: Attribute.REACTION,
    ActiveSkill.PILOT_WALKER: Attribute.REACTION,
    ActiveSkill.PILOT_WATERCRAFT: Attribute.REACTION,
    ActiveSkill.RUNNING: Attribute.STRENGTH,
    ActiveSkill.SWIMMING: Attribute.STRENGTH,
    ActiveSkill.ANIMAL_HANDLING: Attribute.CHARISMA,
    ActiveSkill.CON: Attribute.CHARISMA,
    ActiveSkill.ETIQUETTE: Attribute.CHARISMA,
    ActiveSkill.IMPERSONATION: Attribute.CHARISMA,
    ActiveSkill.INSTRUCTION: Attribute.CHARISMA,
    ActiveSkill.INTIMIDATION: Attribute.CHARISMA,
    ActiveSkill.LEADERSHIP: Attribute.CHARISMA,
    ActiveSkill.NEGOTIATION: Attribute.CHARISMA,
    ActiveSkill.PERFORMANCE: Attribute.CHARISMA,
    ActiveSkill.ARTISAN: Attribute.INTUITION,
    ActiveSkill.ASSENSING: Attribute.INTUITION,
    ActiveSkill.DISGUISE: Attribute.INTUITION,
    ActiveSkill.NAVIGATION: Attribute.INTUITION,
    ActiveSkill.PERCEPTION: Attribute.INTUITION,
    ActiveSkill.TRACKING: Attribute.INTUITION,
    ActiveSkill.AERONAUTICS_MECHANIC: Attribute.LOGIC,
    ActiveSkill.ARCANA: Attribute.LOGIC,
    ActiveSkill.ARMORER: Attribute.LOGIC,
    ActiveSkill.AUTOMOTIVE_MECHANIC: Attribute.LOGIC,
    ActiveSkill.BIOTECHNOLOGY: Attribute.LOGIC,
    ActiveSkill.CHEMISTRY: Attribute.LOGIC,
    ActiveSkill.COMPUTER: Attribute.LOGIC,
    ActiveSkill.CYBERTECHNOLOGY: Attribute.LOGIC,
    ActiveSkill.CYBERCOMBAT: Attribute.LOGIC,
    ActiveSkill.DEMOLITIONS: Attribute.LOGIC,
    ActiveSkill.ELECTRONIC_WARFARE: Attribute.LOGIC,
    ActiveSkill.FIRST_AID: Attribute.LOGIC,
    ActiveSkill.FORGERY: Attribute.LOGIC,
    ActiveSkill.INDUSTRIAL_MECHANIC: Attribute.LOGIC,
    ActiveSkill.HACKING: Attribute.LOGIC,
    ActiveSkill.HARDWARE: Attribute.LOGIC,
    ActiveSkill.MEDICINE: Attribute.LOGIC,
    ActiveSkill.NAUTICAL_MECHANIC: Attribute.LOGIC,
    ActiveSkill.SOFTWARE: Attribute.LOGIC,
    ActiveSkill.ASTRAL_COMBAT: Attribute.WILLPOWER,
    ActiveSkill.SURVIVAL: Attribute.WILLPOWER,
    ActiveSkill.ALCHEMY: Attribute.MAGIC,
    ActiveSkill.ARTIFICING: Attribute.MAGIC,
    ActiveSkill.BANISHING: Attribute.MAGIC,
    ActiveSkill.BINDING: Attribute.MAGIC,
    ActiveSkill.COUNTERSPELLING: Attribute.MAGIC,
    ActiveSkill.DISENCHANTING: Attribute.MAGIC,
    ActiveSkill.RITUAL_SPELLCASTING: Attribute.MAGIC,
    ActiveSkill.SPELLCASTING: Attribute.MAGIC,
    ActiveSkill.SUMMONING: Attribute.MAGIC,
    ActiveSkill.COMPILING: Attribute.RESONANCE,
    ActiveSkill.DECOMPILING: Attribute.RESONANCE,
    ActiveSkill.REGISTERING: Attribute.RESONANCE
}


class CharacterSettings:
    color: t.Optional[int] = None
    do_defaulting: bool = True
    infer_limits: bool = True


class Character:
    server_id: int
    user_id: int

    sheet_url: str
    settings: CharacterSettings

    name: str
    base_attributes: t.Dict[Attribute, t.Union[int, float]]
    skills: t.Dict[ActiveSkill, int]
    max_phys: int
    max_stun: int
    max_overflow: int
    ranged_weapons: t.List[str]
    melee_weapons: t.List[str]
    armor: t.List[str]

    attributes: t.Dict[Attribute, t.Union[int, float]]
    edge_points: int = None
    phys_dmg: int = None
    stun_dmg: int = None
    overflow_dmg: int = None

    def calculate_derived_stats(self):
        self.max_phys = 8 + int(math.ceil(self.attributes[Attribute.BODY] / 2))
        self.max_stun = 8 + int(math.ceil(self.attributes[Attribute.WILLPOWER] / 2))
        self.max_overflow = self.attributes[Attribute.BODY]

        self.phys_dmg = self.phys_dmg or 0
        self.stun_dmg = self.stun_dmg or 0
        self.overflow_dmg = self.overflow_dmg or 0
        self.edge_points = self.edge_points or self.attributes[Attribute.EDGE]

    def update(self):
        try:
            sheet = sheets.get(self.sheet_url)
            assert sheet is not None
        except (ValueError, AssertionError):
            raise ValueError("Sheet not found. Make sure your sheet is shared with synapse5e@gmail.com")
        try:
            attributes_sheet = sheet.find("Attributes")
            skills_sheet = sheet.find("Skills")
            char_sheet_hidden = sheet.find("Character Sheet Hidden")
        except KeyError as e:
            raise ValueError(f"Could not find sheet \"{e.args[0]}\"")

        self.name = sheet.find("Character Sheet")["I8"]

        try:
            self.base_attributes = {
                Attribute.BODY: int(attributes_sheet["C3"]),
                Attribute.AGILITY: int(attributes_sheet["D3"]),
                Attribute.REACTION: int(attributes_sheet["E3"]),
                Attribute.STRENGTH: int(attributes_sheet["F3"]),
                Attribute.WILLPOWER: int(attributes_sheet["G3"]),
                Attribute.LOGIC: int(attributes_sheet["H3"]),
                Attribute.INTUITION: int(attributes_sheet["I3"]),
                Attribute.CHARISMA: int(attributes_sheet["J3"]),
                Attribute.EDGE: int(attributes_sheet["K3"]),
                Attribute.MAGIC: int(attributes_sheet["L3"]),
                Attribute.RESONANCE: int(attributes_sheet["M3"]),
                Attribute.ESSENCE: float(attributes_sheet["N2"]),
            }

            self.attributes = {
                Attribute.BODY: int(attributes_sheet["C2"]),
                Attribute.AGILITY: int(attributes_sheet["D2"]),
                Attribute.REACTION: int(attributes_sheet["E2"]),
                Attribute.STRENGTH: int(attributes_sheet["F2"]),
                Attribute.WILLPOWER: int(attributes_sheet["G2"]),
                Attribute.LOGIC: int(attributes_sheet["H2"]),
                Attribute.INTUITION: int(attributes_sheet["I2"]),
                Attribute.CHARISMA: int(attributes_sheet["J2"]),
                Attribute.EDGE: int(attributes_sheet["K2"]),
                Attribute.MAGIC: int(attributes_sheet["L2"]),
                Attribute.RESONANCE: int(attributes_sheet["M2"]),
                Attribute.ESSENCE: float(attributes_sheet["N2"]),
            }
        except (KeyError, ValueError):
            raise ValueError("Failed to parse attributes")

        self.skills = {}
        for i in range(1, skills_sheet.nrows):
            try:
                name = skills_sheet.at(col=4, row=i)
                rating = skills_sheet.at(col=1, row=i)
            except IndexError:
                continue
            if name != "" and rating != "":
                try:
                    self.skills[ActiveSkill[name.upper().replace(" ", "_")]] = int(rating)
                except (KeyError, ValueError):
                    print(f"Could not parse skill {name}")

        for skill in list(ActiveSkill):
            if skill not in self.skills.keys():
                self.skills[skill] = 0

        self.calculate_derived_stats()

        self.armor = []
        for i in range(0, char_sheet_hidden.nrows):
            try:
                armor = char_sheet_hidden.at(row=i, col=2)
            except IndexError:
                continue
            if armor != "" and not armor.startswith("#"):
                self.armor.append(armor)

        self.melee_weapons = []
        for i in range(0, char_sheet_hidden.nrows):
            try:
                weapon = char_sheet_hidden.at(row=i, col=4)
            except IndexError:
                continue
            if weapon != "" and not weapon.startswith("#"):
                self.melee_weapons.append(weapon)

        self.ranged_weapons = []
        for i in range(0, char_sheet_hidden.nrows):
            try:
                weapon = char_sheet_hidden.at(row=i, col=8)
            except IndexError:
                continue
            if weapon != "" and not weapon.startswith("#"):
                self.ranged_weapons.append(weapon)

    def as_dict(self):
        out_dict = {}
        for k, v in self.__dict__.items():
            out_dict[k] = to_json(v)
        return out_dict

    @classmethod
    def from_dict(cls, d):
        c = Character()
        for k, v in d.items():
            if k == "settings":
                c.settings = CharacterSettings()
                for k2, v2 in v.items():
                    setattr(c.settings, k2, v2)
            elif k in ("base_attributes", "attributes"):
                setattr(c, k, {Attribute[a]: r for a, r in v.items()})
            elif k == "skills":
                c.skills = {ActiveSkill[s]: r for s, r in v.items()}
            else:
                setattr(c, k, v)

        return c

    @classmethod
    def from_url(cls, url: str, server_id: int, user_id: int):
        c = Character()
        c.sheet_url = url
        c.server_id = server_id
        c.user_id = user_id
        c.update()
        c.settings = CharacterSettings()
        return c


def to_json(obj):
    if obj is None or type(obj) in (int, float, str, bool):
        return obj
    if type(obj) == list:
        return [to_json(e) for e in obj]
    if type(obj) == dict:
        d = {}
        for k, v in obj.items():
            d[to_json(k)] = to_json(v)
        return d
    if type(obj) in (Attribute, ActiveSkill):
        return obj.name
    if type(obj) == CharacterSettings:
        return obj.__dict__
    raise ValueError(f"Can't serialize type {type(obj)}")
