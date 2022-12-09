import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from common.constants import DAY_ONE_OF_EACH_MONTH_CRON
from common.utils.dates import DateUtils
from discord.ext import commands
from formatters import timeline


class Timelines(commands.Cog):
    """Hiring events for every month"""

    def __init__(self, bot):
        self.bot = bot
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()

        self.scheduler.add_job(
            self.send_message, CronTrigger.from_crontab(DAY_ONE_OF_EACH_MONTH_CRON)
        )
        self.scheduler.start()

    async def send_message(self):
        channel_id = int(os.environ["ANNOUNCEMENT_CHANNEL_ID"])
        channel = self.bot.get_channel(channel_id)
        print("Cron Happened")
        # print(self.scheduler.get_next_fire_time())
        await channel.send("This is CRONJ")


async def setup(bot):
    """Required setup method"""
    await bot.add_cog(Timelines(bot))
