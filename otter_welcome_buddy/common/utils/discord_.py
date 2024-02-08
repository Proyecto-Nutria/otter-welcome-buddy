import logging

import discord
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_welcome_buddy.common.utils.types.common import DiscordChannelType


logger = logging.getLogger(__name__)


async def send_plain_message(ctx: Context, message: str) -> None:
    """Send a message as embed, this allows to use more markdown features"""
    try:
        await ctx.send(embed=discord.Embed(description=message, color=discord.Color.teal()))
    except discord.Forbidden:
        logger.exception("Not enough permissions to send the message")
    except discord.HTTPException:
        logger.exception("Sending the message failed")


def get_channel_by_id(bot: Bot, channel_id: int) -> DiscordChannelType | None:
    """
    Function to get the a channel by ID
    """
    return bot.get_channel(channel_id) if channel_id else None
