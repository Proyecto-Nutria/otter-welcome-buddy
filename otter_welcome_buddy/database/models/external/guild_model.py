from mongoengine import Document
from mongoengine import IntField


class GuildModel(Document):
    """
    A model that represents a guild (server) in the database.

    Attributes:
        id (int):   The identifier for the guild, is taken from discord records and is the primary
                    key of the object
    """

    id = IntField(primary_key=True, required=True)
