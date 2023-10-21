import os
import re

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_welcome_buddy.common.constants import CronExpressions
from otter_welcome_buddy.common.utils.dates import DateUtils
from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.formatters import englishclub_message


class English(commands.Cog):
    """
    English command events, where notifications about English sessions
    Commands:
        englishclub start:     Start cronjob for timeline messages
        englishclub stop:      Stop cronjob for timeline messages
    """

    def __init__(self, bot: Bot, messages_dependency: type[englishclub_message.Formatter]):
        self.bot: Bot = bot
        self.messages_formatter: type[englishclub_message.Formatter] = messages_dependency
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.__configure_scheduler()

    @commands.group(
        brief="Commands related to English Club!",
        invoke_without_command=True,
        pass_context=True,
    )
    async def englishclub(self, ctx: Context) -> None:
        """
        English Club will setup an English session
        """
        await ctx.send_help(ctx.command)

    @englishclub.command(brief="Start the cronjob for the timeline messages")  # type: ignore
    async def start(self, _: Context) -> None:
        """Command to interact with the bot and start cron"""
        self.__configure_scheduler()

    @englishclub.command(brief="Stop the cronjob for the timeline messages")  # type: ignore
    async def stop(self, _: Context) -> None:
        """Command to interact with the bot and stop cron"""
        self.scheduler.stop()

    @commands.command(brief="Schedule an English session")
    async def schedule_session(self, ctx: Context, hour: str) -> None:
        """Schedule the English Club session"""

        pattern = r"^\d{1,2}:\d{2}(AM|PM)$"

        if re.match(pattern, hour):
            channel_id: int = int(os.environ["ENGLISH_CHANNEL_ID"])
            channel: DiscordChannelType | None = self.bot.get_channel(channel_id)
            description = f"A study session has been scheduled for {hour} on Sunday"

            embed = discord.Embed(
                colour=discord.Colour.green(),
                title="Schedule the English Club session",
                description=description,
            )

            embed.set_image(url="bit.ly/3rZuR6Y")

            if isinstance(channel, TextChannel):
                await channel.send(embed=embed)
        else:
            await ctx.send(
                "Invalid, Use the following format: HH:MMam or HH:MMpm, e.g., '10:00PM'.",
            )

    def _command_message(self) -> Embed:
        """
        Generate an Embed message for the English Club reminder.
        """
        axssel_user_id = int(os.environ["USER_ID"])
        axssel_mention = f"<@{axssel_user_id}>"

        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="English Club Reminder",
            description=f"Hey yo, English club this week? {axssel_mention} 👀",
        )

        return embed

    def __configure_scheduler(self) -> None:
        """Configure and start scheduler"""

        self.scheduler.add_job(
            self.send_message_on_english_non_teachers,
            DateUtils.create_cron_trigger_from(
                CronExpressions.ENGLISH_CLUB_TIME.value,
            ),
        )
        self.scheduler.start()

    async def send_message_on_english_non_teachers(self) -> None:
        """
        Sends message to english_non_teachers channel
        """

        channel_id: int = int(os.environ["ROOT_CHANNEL_ID"])
        channel: DiscordChannelType | None = self.bot.get_channel(channel_id)
        if isinstance(channel, TextChannel):
            await channel.send(embed=self._command_message())
        else:
            raise TypeError("Not valid channel to send the message in")


async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(English(bot, englishclub_message.Formatter))
