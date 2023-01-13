from typing import Type

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from otter_welcome_buddy.formatters import debug, messages


class Greetings(commands.Cog):
    """When a user joins, sends reactionable message"""

    def __init__(
        self,
        bot: Bot,
        messages_dependency: Type[messages.Formatter],
        debug_dependency: Type[debug.Formatter],
    ) -> None:
        self.bot: Bot = bot
        self.messages_formatter: Type[messages.Formatter] = messages_dependency
        self.debug_formatter: Type[debug.Formatter] = debug_dependency

    def _command_message(self) -> str:
        return self.messages_formatter.welcome_message()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Ready Event"""
        print(self.debug_formatter.bot_is_ready())

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Send Welcome message to new member"""
        await member.send(self.messages_formatter.welcome_message())

    @commands.command()
    async def hello(self, ctx: Context) -> None:
        """Sends welcome message with !hello"""
        await ctx.send(self._command_message())


async def setup(bot: Bot) -> None:
    """Required setup method"""
    await bot.add_cog(Greetings(bot, messages.Formatter, debug.Formatter))
