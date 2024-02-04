import re

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_welcome_buddy.common.constants import CronExpressions
from otter_welcome_buddy.common.constants import OTTER_ADMIN
from otter_welcome_buddy.common.constants import OTTER_HEADER_IMAGE
from otter_welcome_buddy.common.constants import OTTER_MODERATOR
from otter_welcome_buddy.common.utils.dates import DateUtils
from otter_welcome_buddy.common.utils.discord_ import get_channel_by_id
from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.formatters import messages
from otter_welcome_buddy.settings import ADMIN_ROLE_ID
from otter_welcome_buddy.settings import COLLABORATOR_ROLE_ID
from otter_welcome_buddy.settings import ENGLISH_CHANNEL_ID
from otter_welcome_buddy.settings import NON_ENGLISH_TEACHERS_CHANNEL_ID

ENGLISH_CLUB_JOB_ID = "0a0575d5-ef2e-4269-acc5-07beb53d1ef0"


class English(commands.Cog):
    """
    English command events, where notifications about English sessions
    Commands:
        englishclub start:               Start cronjob for english club reminders messages
        englishclub stop:                Stop cronjob for english club reminders messages

    schedule_session:    Allows us to schedule an English session
    """

    def __init__(self, bot: Bot, messages_dependency: type[messages.Formatter]):
        self.bot: Bot = bot
        self.messages_formatter: type[messages.Formatter] = messages_dependency
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.__configure_scheduler()

    @commands.group(
        brief="Commands related to English Club!",
        invoke_without_command=True,
        pass_context=True,
    )
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def englishclub(self, ctx: Context) -> None:
        """Displays englishclub commands"""
        await ctx.send_help(ctx.command)

    @englishclub.command(brief="Start the cronjob for the messages")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def start(self, _: Context) -> None:
        """Command to interact with the bot and start cron"""

        self.__configure_scheduler()

    @englishclub.command(brief="Stop the cronjob for the messages")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def stop(self, _: Context) -> None:
        """Command to interact with the bot and stop cron"""

        self.scheduler.remove_job(ENGLISH_CLUB_JOB_ID)

    @commands.command(brief="Schedule an English session")
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def schedule_session(self, ctx: Context, *hour: str) -> None:
        """Schedules the English Club session"""

        # Regex pattern explanation:
        # ^: Asserts the start of the string.
        # (1[0-2]|0?[1-9]): Matches an hour with the 12-hour format.
        # : Matches the colon that separates the hour and minute.
        # ([0-5][0-9]): Matches exactly 2 digits for the minutes, from "00" to "59".
        #  ?: Matches zero or one space, allowing for space between the minutes and AM/PM.
        # (AM|PM): Matches either "AM" or "PM" (case-sensitive).
        # $: Asserts the end of the string.
        time_format_regex = r"^(1[0-2]|0?[1-9]):([0-5][0-9]) ?(AM|PM)$"
        hour_str: str = " ".join(hour)

        if re.match(time_format_regex, hour_str):
            channel_id: int = ENGLISH_CHANNEL_ID
            channel: DiscordChannelType | None = get_channel_by_id(self.bot, channel_id)
            everyone = "@everyone"

            embed = discord.Embed(
                colour=discord.Colour.green(),
                title="English Club Session",
                description=everyone + self.messages_formatter.english_club_message(hour_str),
            )

            embed.set_thumbnail(url=OTTER_HEADER_IMAGE)

            if isinstance(channel, TextChannel):
                await channel.send(embed=embed)
        else:
            await ctx.send(
                "Invalid, Use the following format: HH:MM AM or HH:MM PM, e.g., '10:00 PM'.",
            )

    def _message_non_english_club(self) -> str:
        """
        Generates a message for the English Club reminder.
        """
        adm = ADMIN_ROLE_ID
        col = COLLABORATOR_ROLE_ID
        description = f"{self.messages_formatter.non_english_club_message()} <@&{adm}> <@&{col}> 👀"

        return description

    def __configure_scheduler(self) -> None:
        """Configure and start scheduler"""

        self.scheduler.add_job(
            self._send_message_on_english_non_teachers,
            DateUtils.create_cron_trigger_from(
                CronExpressions.WEDNESDAY_NOON_CRON.value,
            ),
            id=ENGLISH_CLUB_JOB_ID,
        )
        self.scheduler.start()

    async def _send_message_on_english_non_teachers(self) -> None:
        """
        Sends message to english_non_teachers channel
        """

        channel_id: int = NON_ENGLISH_TEACHERS_CHANNEL_ID
        channel: DiscordChannelType | None = get_channel_by_id(self.bot, channel_id)
        if isinstance(channel, TextChannel):
            await channel.send(self._message_non_english_club())
        else:
            raise TypeError("Not valid channel to send the message in")


async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(English(bot, messages.Formatter))
