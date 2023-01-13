
from typing import Type, TypeAlias

import discord


DiscordChannelTypeT: TypeAlias = discord.abc.GuildChannel | discord.Thread | discord.abc.PrivateChannel