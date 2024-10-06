import datetime
import logging

from discord import Color
from discord import Embed
from discord import TextChannel
from discord.abc import Messageable
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_welcome_buddy.common.constants import OTTER_ADMIN
from otter_welcome_buddy.common.constants import OTTER_MODERATOR
from otter_welcome_buddy.common.utils.discord_ import send_plain_message
from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.database.handlers.db_leetcode_config_handler import DbLeetcodeConfigHandler
from otter_welcome_buddy.database.models.external.leetcode_config_model import LeetcodeConfigModel
from otter_welcome_buddy.gql_service.handlers.gql_leetcode_handler import GqlLeetcodeHandler
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeQuestionModel
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeTopicTagModel


logger = logging.getLogger(__name__)


class Leetcode(commands.Cog):
    """
    Refer to this template when adding a new command for the bot,
    once done, call it on the cogs.py file
    Commands:
        leetcode daily_challenge start <text_channel>:  Configure daily challenge announcements
        leetcode daily_challenge stop:                  Stop daily challenge announcements
        leetcode daily_challenge run check:             Manually trigger the daily challenge check
        leetcode daily_challenge run start_task:        Start the daily challenge task
        leetcode daily_challenge run stop_task:         Stop the daily challenge task
    """

    _DAILY_CHALLENGE_TIMES: list[datetime.time] = [
        datetime.time(hour=0, minute=2, tzinfo=datetime.timezone.utc),
    ]
    _LEETCODE_URL: str = "https://leetcode.com"

    def __init__(self, bot: Bot):
        """
        Leetcode command constructor
        """
        self.bot: Bot = bot
        self.daily_challenge_check.start()  # pylint: disable=E1101

    async def cog_unload(self) -> None:
        """
        Override the parent method which is called when the cog is unloaded,
        ensuring that any ongoing tasks related to the daily challenge check
        are properly canceled to prevent any potential issues or memory leaks.
        """
        self.daily_challenge_check.cancel()  # pylint: disable=E1101
        return None

    @commands.group(invoke_without_command=True, aliases=["lc"])
    async def leetcode(self, ctx: Context) -> None:
        """
        Leetcode will send the help when no final command is invoked
        """
        await ctx.send_help(ctx.command)

    @tasks.loop(time=_DAILY_CHALLENGE_TIMES)
    async def daily_challenge_check(self) -> None:
        """
        A task loop that runs daily at specified times to check and process the daily challenge.
        """
        await self._process_daily_challenge()

    async def _get_daily_challenge_embed(self) -> Embed | None:
        """
        Asynchronously generates an embed for the daily LeetCode challenge.

        This method fetches the daily challenge from the LeetCode GraphQL handler,
        constructs an embed with the challenge details, and returns it. If no daily
        challenge or question is found, it logs a warning and returns None.
        """
        daily_challenge = await GqlLeetcodeHandler.gen_daily_challenge()
        if daily_challenge is None:
            logger.warning("No daily challenge found")
            return None
        question: LeetcodeQuestionModel | None = daily_challenge.question
        if question is None:
            logger.warning("No question found in daily challenge")
            return None
        tags: list[LeetcodeTopicTagModel] | None = question.topic_tags
        if tags is None:
            logger.warning("No tags found in daily challenge question")
            tags = []
        embed = Embed(
            title=question.title,
            url=f"{self._LEETCODE_URL}{daily_challenge.link}",
            color=Color.teal(),
        )
        embed.add_field(name="Difficulty", value=question.difficulty, inline=False)
        embed.add_field(
            name="Tags",
            value=" ".join(f"`{tag.name}`" for tag in tags),
            inline=False,
        )
        embed.set_footer(text=f"Date: {daily_challenge.date}")
        return embed

    async def _process_daily_challenge(self) -> None:
        """
        Asynchronously processes the daily challenge by generating an embed and sending it to
        configured channels retrieved from the database.
        """
        embed: Embed | None = await self._get_daily_challenge_embed()
        if embed is None:
            logger.warning("Embed generation failed for daily challenge")
            return
        leetcode_config_models: list[
            LeetcodeConfigModel
        ] = DbLeetcodeConfigHandler.get_all_leetcode_configs()
        for leetcode_config_model in leetcode_config_models:
            channel: DiscordChannelType | None = self.bot.get_channel(
                leetcode_config_model.channel_id,
            )
            if channel is None:
                logger.warning("Channel not found for guild %s", leetcode_config_model.guild.id)
                continue
            if isinstance(channel, Messageable):
                await channel.send(
                    "New **daily challenge** has appeared, you have **24hrs** to solve it!",
                    embed=embed,
                )

    @leetcode.group(invoke_without_command=True, aliases=["daily"])  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def daily_challenge(self, ctx: Context) -> None:
        """
        Leetcode will send the help when no final command is invoked
        """
        await ctx.send_help(ctx.command)

    @daily_challenge.command(  # type: ignore
        brief="Start the daily activity check subscribing to the announcements",
        usage="<text_channel>",
    )
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def start(
        self,
        ctx: Context,
        channel: TextChannel,
    ) -> None:
        """Starts the daily challenge task."""
        if ctx.guild is None:
            logger.warning("No guild on context to start")
            return

        leetcode_config_model: LeetcodeConfigModel | None = (
            DbLeetcodeConfigHandler.get_leetcode_config(
                guild_id=ctx.guild.id,
            )
        )
        if leetcode_config_model is None:
            leetcode_config_model = LeetcodeConfigModel(
                guild=ctx.guild.id,
            )
        leetcode_config_model.channel_id = channel.id

        try:
            DbLeetcodeConfigHandler.insert_leetcode_config(
                leetcode_config_model=leetcode_config_model,
            )
            await send_plain_message(
                ctx,
                "**Leetcode Daily Challenge** subscribed, be ready to practice!",
            )
        except Exception:
            logger.exception("Error while inserting into database")

    @daily_challenge.command(brief="Stop the daily activity announcements")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def stop(self, ctx: Context) -> None:
        """Stop the daily challenge task."""
        if ctx.guild is None:
            logger.warning("No guild on context")
            return

        try:
            leetcode_config = DbLeetcodeConfigHandler.get_leetcode_config(
                guild_id=ctx.guild.id,
            )
            msg: str = ""
            if leetcode_config is not None:
                DbLeetcodeConfigHandler.delete_leetcode_config(guild_id=ctx.guild.id)
                msg = "**Leetcode config** removed!"
            else:
                msg = "No config set! 😱"
            await send_plain_message(ctx, msg)
        except Exception:
            logger.exception("Error while deleting from database")

    @daily_challenge.group(  # type: ignore
        brief="Commands related to trigger manually the Leetcode daily challenge check",
        invoke_without_command=True,
    )
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def run(self, ctx: Context) -> None:
        """
        Admin commands related to trigger and test the check
        """
        await ctx.send_help(ctx.command)

    @run.command(brief="Admin command to trigger the daily challenge check")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def check(self, _: Context) -> None:
        """
        Admin command that execute the check daily challenge
        """
        await self._process_daily_challenge()

    @run.command(brief="Admin command to start the daily challenge task")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def start_task(self, ctx: Context) -> None:
        """
        Admin command to start the daily challenge task
        """
        is_task_running: bool = self.daily_challenge_check.is_running()  # pylint: disable=E1101
        if is_task_running:
            await ctx.send("Daily challenge check is already running.")
            return
        self.daily_challenge_check.start()  # pylint: disable=E1101

    @run.command(brief="Admin command to stop the daily challenge task")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def stop_task(self, _: Context) -> None:
        """
        Admin command to stop the daily challenge task
        """
        self.daily_challenge_check.cancel()  # pylint: disable=E1101


async def setup(bot: Bot) -> None:
    """Required setup method"""
    await bot.add_cog(Leetcode(bot))
