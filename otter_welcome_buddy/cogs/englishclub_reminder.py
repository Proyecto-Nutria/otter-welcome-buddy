import os
import re

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_welcome_buddy.common.constants import CronExpressions
from otter_welcome_buddy.common.discord_channel import DiscordChannel
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
    @commands.check(is_allowed)
    async def englishclub(self, ctx: Context) -> None:
        """
        English Club will setup an English session
        """
        await ctx.send_help(ctx.command)

    @englishclub.command(brief="Start the cronjob for the messages")  # type: ignore
    @commands.check(is_allowed)
    async def start(self, _: Context) -> None:
        """Command to interact with the bot and start cron"""
        self.__configure_scheduler()

    @englishclub.command(brief="Stop the cronjob for the messages")  # type: ignore
    @commands.check(is_allowed)
    async def stop(self, _: Context) -> None:
        """Command to interact with the bot and stop cron"""
        self.scheduler.remove_job("job_id")

    @commands.command(brief="Schedule an English session")
    @commands.check(is_allowed)
    async def schedule_session(self, ctx: Context, hour: str) -> None:
        """Schedule the English Club session"""

        # Regex pattern explanation:
        # ^: Asserts the start of the string.
        # \d{1,2}: Matches 1 or 2 digits, representing the hour (e.g., 1, 10, or 12).
        # : Matches the colon that separates the hour and minute.
        # \d{2}: Matches exactly 2 digits, representing the minutes (e.g., 00, 30, or 59).
        # (AM|PM): Matches either "AM" or "PM" (case-sensitive).
        # $: Asserts the end of the string.
        time_format_regex = r"^\d{1,2}:\d{2}(AM|PM)$"

        if re.match(time_format_regex, hour):
            channel_id: int = DiscordChannel.ENGLISH_CHANNEL_ID.value
            channel: DiscordChannelType | None = (
                DiscordChannel.ENGLISH_CHANNEL_ID.get_discord_channel(
                    self.bot,
                    channel_id,
                )
            )
            mention = "@everyone"

            embed = discord.Embed(
                colour=discord.Colour.green(),
                title="English Club session",
                description=mention + self.messages_formatter.english_club_message(hour),
            )

            embed.set_image(url=DiscordChannel.ENGLISH_CHANNEL_IMAGE.value)

            if isinstance(channel, TextChannel):
                await channel.send(embed=embed)
        else:
            await ctx.send(
                "Invalid, Use the following format: HH:MMAM or HH:MMPM, e.g., '10:00PM'.",
            )

    def message_non_english_club(self) -> str:
        """
        Generate an Embed message for the English Club reminder.
        """

        user_1 = f"<@{os.environ['USER_ONE_ID']}>"
        user_2 = f"<@{os.environ['USER_TWO_ID']}>"
        description = f"{self.messages_formatter.non_english_club_message()} {user_1} {user_2} 👀"

        return description

    def __configure_scheduler(self) -> None:
        """Configure and start scheduler"""

        self.scheduler.add_job(
            self.send_message_on_english_non_teachers,
            DateUtils.create_cron_trigger_from(
                CronExpressions.NON_ENGLISH_TEACHERS_MESSAGE_TIME.value,
            ),
            id="job_id",
        )
        self.scheduler.start()

    async def send_message_on_english_non_teachers(self) -> None:
        """
        Sends message to english_non_teachers channel
        """

        channel_id: int = DiscordChannel.NON_ENGLISH_TEACHERS_CHANNEL_ID.value
        channel: DiscordChannelType | None = (
            DiscordChannel.NON_ENGLISH_TEACHERS_CHANNEL_ID.get_discord_channel(
                self.bot,
                channel_id,
            )
        )
        if isinstance(channel, TextChannel):
            await channel.send(self.message_non_english_club())
        else:
            raise TypeError("Not valid channel to send the message in")


async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(English(bot, englishclub_message.Formatter))
