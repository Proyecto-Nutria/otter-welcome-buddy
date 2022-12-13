import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

from otter_welcome_buddy.common.constants import DAY_ONE_OF_EACH_MONTH_CRON
from otter_welcome_buddy.common.utils.dates import DateUtils
from otter_welcome_buddy.formatters import timeline


class Timelines(commands.Cog):
    """Hiring events for every month"""

    def __init__(self, bot, messages_formatter):
        self.bot = bot
        self.messages_formatter = messages_formatter
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.__configure_scheduler()

    def __configure_scheduler(self):
        """Configure and start scheduler"""
        self.scheduler.add_job(
            self.send_message_on_channel,
            DateUtils.create_cron_trigger_from(DAY_ONE_OF_EACH_MONTH_CRON),
        )
        self.scheduler.start()

    async def send_message_on_channel(self):
        """Sends message to announcement channel at the start of month"""
        channel_id = int(os.environ["ANNOUNCEMENT_CHANNEL_ID"])
        channel = self.bot.get_channel(channel_id)
        message = self.messages_formatter.get_hiring_events_for(
            DateUtils.get_current_month()
        )
        await channel.send(message)


async def setup(bot):
    """Required setup method"""
    await bot.add_cog(Timelines(bot, timeline.Formatter))
