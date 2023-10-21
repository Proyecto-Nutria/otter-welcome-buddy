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


def is_allowed(ctx: Context) -> bool:
    """
    Return if a user is allowed to run a command or not
    """
    return ctx.author.id == int(os.environ["USER_ONE_ID"]) or ctx.author.id == int(
        os.environ["USER_TWO_ID"],
    )


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

    @englishclub.command(brief="Start the cronjob for the messages")  # type: ignore
    async def start(self, _: Context) -> None:
        """Command to interact with the bot and start cron"""
        self.__configure_scheduler()

    @englishclub.command(brief="Stop the cronjob for the messages")  # type: ignore
    async def stop(self, _: Context) -> None:
        """Command to interact with the bot and stop cron"""
        self.scheduler.remove_job("job_id")

    @commands.command(brief="Schedule an English session")
    @commands.check(is_allowed)
    async def schedule_session(self, ctx: Context, hour: str) -> None:
        """Schedule the English Club session"""

        pattern = r"^\d{1,2}:\d{2}(AM|PM)$"

        if re.match(pattern, hour):
            channel_id: int = int(os.environ["ENGLISH_CHANNEL_ID"])
            channel: DiscordChannelType | None = self.bot.get_channel(channel_id)
            mention = "@everyone"

            embed = discord.Embed(
                colour=discord.Colour.blue(),
                title="English Club session",
                description=mention + self.messages_formatter.english_club_message(hour),
            )

            embed.set_image(url="https://shorturl.at/blqMV")

            if isinstance(channel, TextChannel):
                await channel.send(embed=embed)
        else:
            await ctx.send(
                "Invalid, Use the following format: HH:MMam or HH:MMpm, e.g., '10:00PM'.",
            )

    def message_non_english_club(self) -> Embed:
        """
        Generate an Embed message for the English Club reminder.
        """

        user_1 = f"<@{os.environ['USER_ONE_ID']}>"
        user_2 = f"<@{os.environ['USER_TWO_ID']}>"

        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="English Club Reminder",
            description=f"{self.messages_formatter.non_english_club_message()} {user_1} {user_2} 👀",
        )

        return embed

    def __configure_scheduler(self) -> None:
        """Configure and start scheduler"""

        self.scheduler.add_job(
            self.send_message_on_english_non_teachers,
            DateUtils.create_cron_trigger_from(
                CronExpressions.ENGLISH_CLUB_TIME.value,
            ),
            id="job_id",
        )
        self.scheduler.start()

    async def send_message_on_english_non_teachers(self) -> None:
        """
        Sends message to english_non_teachers channel
        """

        channel_id: int = int(os.environ["ROOT_CHANNEL_ID"])
        channel: DiscordChannelType | None = self.bot.get_channel(channel_id)
        if isinstance(channel, TextChannel):
            await channel.send(embed=self.message_non_english_club())
        else:
            raise TypeError("Not valid channel to send the message in")


async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(English(bot, englishclub_message.Formatter))
