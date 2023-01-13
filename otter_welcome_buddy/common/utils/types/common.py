from typing import TypeAlias

import discord

DiscordChannelTypeT: TypeAlias = (
    discord.abc.GuildChannel | discord.Thread | discord.abc.PrivateChannel
)
