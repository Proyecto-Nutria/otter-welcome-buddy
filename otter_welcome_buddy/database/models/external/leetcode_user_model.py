from mongoengine import CASCADE
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import ReferenceField
from otter_welcome_buddy.database.models.external.guild_model import GuildModel

from otter_welcome_buddy.database.models.external.user_model import UserModel


class LeetcodeUserModel(Document):
    """
    A model that represents a leetcode user in the database.

    Attributes:
        handle (str):       Primary key that represents the username of an user in leetcode
        rating (int):       Ranking of the user in leetcode
        user_avatar (str):  Url that shows the user avatar in leetcode
    """

    handle = StringField(primary_key=True, required=True)
    user_avatar = StringField(required=True)
    rating = IntField(required=True)


class LeetcodeChallengeRelation(Document):
    """
    A model that represents a relationship between a user and a guild in the database.

    Attributes:
        user (UserModel):   Primary reference to the user
        guild (GuildModel): Reference to the guild that the user belongs to
    """

    user = ReferenceField(UserModel, reverse_delete_rule=CASCADE, required=True, unique_with="guild")
    guild = ReferenceField(GuildModel, reverse_delete_rule=CASCADE, required=True)
    user = ReferenceField(UserModel, reverse_delete_rule=CASCADE, required=True, unique_with="guild")
