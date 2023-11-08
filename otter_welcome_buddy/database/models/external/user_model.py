from mongoengine import CASCADE
from mongoengine import Document
from mongoengine import IntField
from mongoengine import ReferenceField


class UserModel(Document):
    """
    A model that represents a user in the database.

    Attributes:
        user_id (int):      The identifier for the user, is taken from discord records and is
                            the primary key of the object along with the guild
        guild (GuildModel): Reference to the guild that the user belongs to
    """

    user_id = IntField(required=True, unique_with="guild")
    guild = ReferenceField("GuildModel", reverse_delete_rule=CASCADE, required=True)
