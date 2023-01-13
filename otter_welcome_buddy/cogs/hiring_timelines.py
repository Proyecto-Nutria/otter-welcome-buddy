import os
from typing import Optional, Type

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot, Context

from otter_welcome_buddy.common.constants import CronExpressions
from otter_welcome_buddy.common.utils.dates import DateUtils
from otter_welcome_buddy.common.utils.types.common import DiscordChannelTypeT
from otter_welcome_buddy.formatters import timeline


class Timelines(commands.Cog):
    """Hiring events for every month"""

    def __init__(self, bot: Bot, messages_formatter: Type[timeline.Formatter]):
        self.bot: Bot = bot
        self.messages_formatter: Type[timeline.Formatter] = messages_formatter
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()

    @commands.group(
        brief="Commands related to Timelines messages!",
        invoke_without_command=True,
        pass_context=True,
    )
    async def timelines(self, ctx: Context) -> None:
        """
        Timelines will help to keep track of important events to be announced via cronjobs
        """
        await ctx.send_help(ctx.command)

    @timelines.command(brief="Start the cronjob for the timeline messages")  # type: ignore
    async def start(self, _: Context) -> None:
        """Command to interact with the bot and start cron"""
        self.__configure_scheduler()

    @timelines.command(brief="Stop the cronjob for the timeline messages")  # type: ignore
    async def stop(self, _: Context) -> None:
        """Command to interact with the bot and stop cron"""
        self.scheduler.stop()

    def __configure_scheduler(self) -> None:
        """Configure and start scheduler"""
        self.scheduler.add_job(
            self.send_message_on_channel,
            DateUtils.create_cron_trigger_from(
                CronExpressions.DAY_ONE_OF_EACH_MONTH_CRON.value,
            ),
        )
        self.scheduler.start()

    def _get_hiring_events(self) -> str:
        """Get hiring events for current month"""
        return self.messages_formatter.get_hiring_events_for(
            DateUtils.get_current_month(),
        )

    async def send_message_on_channel(self) -> None:
        """Sends message to announcement channel at the start of month"""
        channel_id: int = int(os.environ["ANNOUNCEMENT_CHANNEL_ID"])
        channel: Optional[DiscordChannelTypeT] = self.bot.get_channel(channel_id)
        if isinstance(channel, TextChannel):
            await channel.send(self._get_hiring_events())
        else:
            raise TypeError("Not valid channel to send the message in")


async def setup(bot: Bot) -> None:
    """Required setup method"""
    await bot.add_cog(Timelines(bot, timeline.Formatter))
