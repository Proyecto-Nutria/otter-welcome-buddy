from mongoengine import CASCADE
from mongoengine import Document
from mongoengine import IntField
from mongoengine import ReferenceField

from otter_welcome_buddy.database.models.external.guild_model import GuildModel


class LeetcodeConfigModel(Document):
    """
    A model that contains the configuration for the Leetcode features interaction.

    Attributes:
        guild (GuildModel):     Reference to the guild that interacts with Leetcode
        channel_id (int):       Channel identifier where to send the announcements
    """

    guild = ReferenceField(GuildModel, reverse_delete_rule=CASCADE, primary_key=True)
    channel_id = IntField(required=True)
