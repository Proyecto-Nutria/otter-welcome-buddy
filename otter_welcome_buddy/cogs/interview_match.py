import asyncio
import datetime
import logging
import random

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_welcome_buddy.common.constants import OTTER_ADMIN
from otter_welcome_buddy.common.constants import OTTER_MODERATOR
from otter_welcome_buddy.common.constants import OTTER_ROLE
from otter_welcome_buddy.common.utils.discord_ import send_plain_message
from otter_welcome_buddy.common.utils.image import create_match_image
from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.database.handlers.db_interview_match_handler import DbInterviewMatchHandler
from otter_welcome_buddy.database.models.external.interview_match_model import InterviewMatchModel
from otter_welcome_buddy.settings import BOT_TIMEZONE


logger = logging.getLogger(__name__)


_CRONJOB_HOUR: int = 12
_DEFAULT_DAY_OF_THE_WEEK: int = 2


class InterviewMatch(commands.Cog):
    """
    Interview Match command activity, where members receive a random buddy to practice with
    Commands:
        interview_match start <text_channel> [day_of_week]:     Start interview match activity
        interview_match stop:                                   Stop interview match activity
        interview_match run send:           Admin command to trigger the send weekly message job
        interview_match run check:          Admin command to trigger the check weekly message job
    """

    _ACTIVITY_MESSAGE: str = (
        "{role_to_mention}\n"
        "Hello my beloved otters, it is time to practice!\n"
        "React to this message with {emoji} if you"
        " want to make a mock interview with another otter.\n"
        "Remember you only have 24 hours to react. A nice week "
        "to all of you and keep coding!"
    )

    _NOTIFICATION_MESSAGE: str = (
        "These are the pairs of the week.\n" "Please get in touch with your partner!"
    )

    _PRIVATE_MESSAGE: str = (
        "Hello {username_one}!\n"
        "You have been paired with {username_two}. Please get in contact with "
        "her/him and don't forget to request the resume!.\n"
        "*Have fun!*\n\n"
        "Check this message for more information about the activity:\n"
        "https://discord.com/channels/742890088190574634/"
        "743138942035034164/859236992403374110"
    )

    def __init__(self, bot: Bot) -> None:
        """
        Interview Match command constructor
        """
        self.bot: Bot = bot
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self.emoji: str = "👍"

        self.scheduler.add_job(
            self._send_weekly_message,
            CronTrigger(hour=_CRONJOB_HOUR, timezone=BOT_TIMEZONE),
            misfire_grace_time=None,
        )
        self.scheduler.add_job(
            self._check_weekly_message,
            CronTrigger(hour=_CRONJOB_HOUR, timezone=BOT_TIMEZONE),
            misfire_grace_time=None,
        )
        self.scheduler.start()

    @commands.group(
        brief="Commands related to Interview Match activity!",
        invoke_without_command=True,
    )
    async def interview_match(self, ctx: Context) -> None:
        """
        Interview Match will help to set up interviews between discord members.
        """
        await ctx.send_help(ctx.command)

    async def _send_weekly_message(self) -> None:
        """
        Check the database to see if any guild is candidate to receive the weekly message,
        if any, send it and store the message id on the database
        """
        weekday: int = datetime.datetime.today().weekday()
        for entry in DbInterviewMatchHandler.get_day_interview_matches(
            weekday=weekday,
        ):
            guild: discord.Guild | None = None
            role: discord.Role | None = None
            try:
                guild = next(guild for guild in self.bot.guilds if guild.id == entry.guild.id)
                role = discord.utils.get(guild.roles, name=OTTER_ROLE)
                if role is None:
                    logger.warning("Not role found in %s for guild %s", __name__, guild.name)
            except StopIteration:
                logger.error("Not guild found in %s", __name__)
            finally:
                interview_buddy_message: str = self._ACTIVITY_MESSAGE.format(
                    role_to_mention=role.mention if role is not None else "",
                    emoji=entry.emoji,
                )
                channel: DiscordChannelType | None = self.bot.get_channel(entry.channel_id)
                if channel is None:
                    logger.error("Fail getting the channel to send the weekly message")
                if not isinstance(channel, discord.TextChannel):
                    raise TypeError("Not valid channel to send the message in")

                message: discord.Message = await channel.send(
                    interview_buddy_message,
                )
                await message.add_reaction(entry.emoji)
                entry.message_id = message.id
                try:
                    DbInterviewMatchHandler.insert_interview_match(
                        interview_match_model=entry,
                    )
                except Exception:
                    logger.exception("Fail updating the entry on the database")

    async def _process_weekly_message(
        self,
        channel: discord.TextChannel,
        week_otter_pool: list[discord.Member],
        placeholder: discord.Member,
    ) -> None:
        """
        Process the candidates from the weekly message to make the pairs and send the
        messages about the activity to them
        """
        try:
            week_otter_pairs: list[tuple[discord.Member, discord.Member]] = self._make_pairs(
                week_otter_pool,
                placeholder,
            )
            _img, img_path = create_match_image(week_otter_pairs)
            for otter_one, otter_two in week_otter_pairs:
                await self._send_pair_message(
                    otter_one=otter_one,
                    otter_two=otter_two,
                )
                await self._send_pair_message(
                    otter_one=otter_two,
                    otter_two=otter_one,
                )

            week_otter_pool.sort(
                key=lambda user: user.display_name,
            )  # in-place sort
            users_mentions: str = ",".join(
                list(map(lambda user: f"{user.mention}", week_otter_pool)),
            )
            message: str = self._NOTIFICATION_MESSAGE
            message += f"\n{users_mentions}"
            await channel.send(message, file=discord.File(img_path))

        except discord.Forbidden:
            logger.exception("Not enough permissions to send the weekly message")
        except discord.HTTPException:
            logger.exception("Sending the message failed")
        except ValueError:
            logger.exception("The weekly pairs image doesn't have the appropriate size")

    async def _check_weekly_message(self, weekday: int | None = None) -> None:
        """
        Check the database to see if any guild is candidate to check the weekly message, if any,
        get the weekly message, get the reactions and process the candidates to make the pairs
        """
        weekday = (datetime.datetime.today().weekday() - 1 + 7) % 7 if weekday is None else weekday

        try:
            for entry in DbInterviewMatchHandler.get_day_interview_matches(
                weekday=weekday,
            ):
                fetched_values: tuple | None = await self._get_weekly_message(
                    channel_id=entry.channel_id,
                    message_id=entry.message_id,
                    author_id=entry.author_id,
                )
                if fetched_values is None:
                    return
                channel: discord.TextChannel
                cache_message: discord.Message
                placeholder: discord.Member
                channel, cache_message, placeholder = fetched_values

                week_otter_pool: list[discord.Member] = await self._get_weekly_pool(
                    message=cache_message,
                    emoji=entry.emoji,
                )
                if not week_otter_pool:
                    await channel.send("No one wanted to practice 😟")
                    logger.info("Empty pool for Interview Match")
                    continue

                await self._process_weekly_message(
                    channel=channel,
                    week_otter_pool=week_otter_pool,
                    placeholder=placeholder,
                )

        except Exception as ex:
            logger.exception("Exception %s in %s", ex, __name__)

    async def _get_weekly_message(
        self,
        channel_id: int,
        message_id: int,
        author_id: int,
    ) -> tuple[discord.TextChannel, discord.Message, discord.Member] | None:
        try:
            channel: DiscordChannelType | None = self.bot.get_channel(channel_id)
            if channel is None:
                logger.error("No channel to check the weekly message")
                return None
            if not isinstance(channel, discord.TextChannel):
                logger.warning("Not valid channel to send the message in")
                return None
            cache_message = await channel.fetch_message(message_id)

            placeholder: discord.Member | None = channel.guild.get_member(author_id)
            if placeholder is None:
                # TODO: add a fallback when no placeholder
                logger.error("No placeholder found for weekly check")
                return None

            return channel, cache_message, placeholder

        except discord.NotFound:
            logger.exception("No message found to be checked")
        except discord.Forbidden:
            logger.exception("Not enough permissions to retrieve weekly message")
        except discord.HTTPException:
            logger.exception("Retrieving the message failed")

        return None

    async def _get_weekly_pool(
        self,
        message: discord.Message,
        emoji: str,
    ) -> list[discord.Member]:
        week_otter_pool_unique: set[discord.Member] = set()
        for reaction in message.reactions:
            if reaction.emoji != emoji:
                continue
            async for user in reaction.users():
                # If the user is not an instance of Member, it almost sure means that
                # no longer belongs to the guild so we don't want to include it
                if isinstance(user, discord.Member) and not user.bot:
                    week_otter_pool_unique.add(user)

        week_otter_pool: list[discord.Member] = list(
            week_otter_pool_unique,
        )

        return week_otter_pool

    async def _send_pair_message(
        self,
        otter_one: discord.Member,
        otter_two: discord.Member,
    ) -> None:
        """
        Receive a pair for the activity, send the message about the activity to them letting
        them know who is their matched pair and how to do the activity
        """
        username_one: str = f"{otter_one.name}#{otter_one.discriminator}"
        username_two: str = f"{otter_two.name}#{otter_two.discriminator}"
        message: str = self._PRIVATE_MESSAGE.format(
            username_one=username_one,
            username_two=username_two,
        )
        try:
            await otter_one.send(message)
        except discord.Forbidden:
            logger.exception("Not enough permissions to send the message to %s", username_one)
        except discord.HTTPException:
            logger.exception("Sending the message to %s failed", username_one)

    def _make_pairs(
        self,
        week_otter_pool: list[discord.Member],
        placeholder: discord.Member,
    ) -> list[tuple[discord.Member, discord.Member]]:
        """
        Receive a list of users, if it's odd, add the wildcard user (usually the user who started
        the activity) and do the pairs shuffling the list and picking the users in consecutive order
        """
        week_otter_pairs: list[tuple[discord.Member, discord.Member]] = []
        week_otter_collaborator: list[discord.Member] = []
        week_otter_member: list[discord.Member] = []
        if len(week_otter_pool) % 2 == 1:
            week_otter_pool.append(placeholder)

        for otter in week_otter_pool:
            otter_roles: list[str] = [str(otter_role) for otter_role in otter.roles]
            if OTTER_MODERATOR in otter_roles or OTTER_ADMIN in otter_roles:
                week_otter_collaborator.append(otter)
            else:
                week_otter_member.append(otter)

        random.shuffle(week_otter_collaborator)
        random.shuffle(week_otter_member)

        # Pair interviewees with collaborators
        collaborator_index = 0
        member_index = 0
        while collaborator_index < len(week_otter_collaborator) and member_index < len(
            week_otter_member,
        ):
            week_otter_pairs.append(
                (week_otter_collaborator[collaborator_index], week_otter_member[member_index]),
            )
            collaborator_index += 1
            member_index += 1

        # Pair additional collaborators
        for idx in range(collaborator_index, len(week_otter_collaborator), 2):
            week_otter_pairs.append(
                (week_otter_collaborator[idx], week_otter_collaborator[idx + 1]),
            )

        # Pair additional members
        for idx in range(member_index, len(week_otter_member), 2):
            week_otter_pairs.append((week_otter_member[idx], week_otter_member[idx + 1]))

        return week_otter_pairs

    @interview_match.command(  # type: ignore
        brief="Start interview match activity",
        usage="<text_channel> [day_of_week]",
    )
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def start(
        self,
        ctx: Context,
        channel: discord.TextChannel,
        day_of_week: int = _DEFAULT_DAY_OF_THE_WEEK,
    ) -> None:
        """
        Start Interview Match setting up options
        """
        if ctx.guild is None:
            logger.warning("No guild on context to start the activity")
            return
        emoji_selected: str = self.emoji
        get_emoji_message: str = (
            "You have 15s to react to this message with the emoji "
            f"that you want to use (by default is {emoji_selected})."
        )
        emoji_message: discord.Message = await ctx.send(get_emoji_message)

        def check(reaction: discord.Reaction, user: discord.Member | discord.User) -> bool:
            return reaction.message.id == emoji_message.id and user == ctx.author

        try:
            reaction: discord.Reaction
            _: discord.Member | discord.User
            reaction, _ = await self.bot.wait_for(
                "reaction_add",
                timeout=15,
                check=check,
            )
            if isinstance(reaction.emoji, str):
                emoji_selected = str(reaction.emoji)
            else:
                # TODO: Add support for custom emojis
                await ctx.send("This is shameful, but currently we don't support custom emojis 😔")
                return
        except asyncio.TimeoutError:
            logger.info("User not reacted to interview_match start")

        interview_match_model = InterviewMatchModel(
            guild=ctx.guild.id,
            author_id=ctx.author.id,
            channel_id=channel.id,
            day_of_the_week=day_of_week % 7,
            emoji=emoji_selected,
            message_id=None,
        )

        try:
            DbInterviewMatchHandler.insert_interview_match(
                interview_match_model=interview_match_model,
            )
            await send_plain_message(
                ctx,
                f"**Interview Match** activity scheduled! See you there {emoji_selected}.",
            )
        except Exception:
            logger.exception("Error while inserting into database")

    @interview_match.command(brief="Stop interview match activity")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def stop(self, ctx: Context) -> None:
        """
        Stop Interview Match
        """
        try:
            if ctx.guild is None:
                logger.warning("No guild on context")
                return
            interview_match_model = DbInterviewMatchHandler.get_interview_match(
                guild_id=ctx.guild.id,
            )
            msg: str = ""
            if interview_match_model is not None:
                DbInterviewMatchHandler.delete_interview_match(guild_id=ctx.guild.id)
                msg = "**Interview Match** activity stopped!"
            else:
                msg = "No activity was running! 😱"
            await send_plain_message(ctx, msg)
        except Exception:
            logger.exception("Error while inserting into database")

    @interview_match.group(  # type: ignore
        brief="Commands related to trigger manually the Interview Match activity!",
        invoke_without_command=True,
    )
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def run(self, ctx: Context) -> None:
        """
        Admin commands related to trigger and test the activity
        """
        await ctx.send_help(ctx.command)

    @run.command(brief="Admin command to trigger the send weekly message job")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def send(self, _: Context) -> None:
        """
        Admin command that execute the send weekly message method, this is executed as usual
        to all the guilds and for the current day
        """
        await self._send_weekly_message()

    @run.command(brief="Admin command to trigger the check weekly message job")  # type: ignore
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def check(self, _: Context) -> None:
        """
        Admin command that execute the check weekly message method, this is executed as usual
        to all the guilds and for the current day
        """
        await self._check_weekly_message(datetime.datetime.today().weekday())


async def setup(bot: Bot) -> None:
    """Required setup method"""
    await bot.add_cog(InterviewMatch(bot=bot))
