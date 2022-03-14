import pymongo
import typing as t

from character import Character

dbClient = pymongo.MongoClient("mongodb://localhost:27017/")

db = dbClient["synapse"]
characters = db["characters"]


def load_character(server_id: int, user_id: id) -> t.Optional[Character]:
    doc = characters.find_one({"server_id": server_id, "user_id": user_id})
    if doc is None:
        return None
    return Character.from_dict(doc)


def save_character(character: Character) -> None:
    characters.replace_one({"server_id": character.server_id, "user_id": character.user_id}, character.as_dict(),
                           upsert=True)
