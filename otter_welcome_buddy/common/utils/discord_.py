from discord.ext.commands import Bot

from otter_welcome_buddy.common.utils.types.common import DiscordChannelType


def get_channel_by_id(bot: Bot, channel_id: int) -> DiscordChannelType | None:
    """
    Function to get the a channel by ID
    """
    return bot.get_channel(channel_id) if channel_id else None
