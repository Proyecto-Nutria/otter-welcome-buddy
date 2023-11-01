import os
from enum import Enum

from discord.ext.commands import Bot
from dotenv import load_dotenv

from otter_welcome_buddy.common.utils.types.common import DiscordChannelType

load_dotenv()


class DiscordChannel(Enum):
    """
    Enum to store Discord channels variables
    """

    ENGLISH_CHANNEL_ID = int(os.environ["GENERAL_CHANNEL_ID"])
    NON_ENGLISH_TEACHERS_CHANNEL_ID = int(os.environ["ROOT_CHANNEL_ID"])
    ENGLISH_CHANNEL_IMAGE = "https://shorturl.at/blqMV"

    def get_discord_channel(self, bot: Bot, channel_id: int) -> DiscordChannelType | None:
        """
        Function to get the a channel by ID
        """
        return bot.get_channel(channel_id) if channel_id else None
