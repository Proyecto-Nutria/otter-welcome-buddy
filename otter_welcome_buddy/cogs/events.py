import logging

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from otter_welcome_buddy.common.constants import OTTER_ROLE
from otter_welcome_buddy.common.constants import WELCOME_MESSAGES
from otter_welcome_buddy.database.handlers.db_guild_handler import DbGuildHandler
from otter_welcome_buddy.database.models.external.guild_model import GuildModel
from otter_welcome_buddy.formatters import debug
from otter_welcome_buddy.startup.database import init_guild_table


logger = logging.getLogger(__name__)


class BotEvents(commands.Cog):
    """Actions related to the events emitted by discord"""

    def __init__(
        self,
        bot: Bot,
        debug_dependency: type[debug.Formatter],
    ) -> None:
        self.bot: Bot = bot
        self.debug_formatter: type[debug.Formatter] = debug_dependency

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Ready Event"""
        init_guild_table(self.bot)

        logger.info(self.debug_formatter.bot_is_ready())

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Event fired when a guild is either created or the bot join into"""
        if DbGuildHandler.get_guild(guild_id=guild.id) is None:
            guild_model: GuildModel = GuildModel(guild_id=guild.id)
            DbGuildHandler.insert_guild(guild_model=guild_model)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """Event fired when a guild is deleted or the bot is removed from it"""
        DbGuildHandler.delete_guild(guild_id=guild.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        """Event fired when a user react to the welcome message, giving the entry role to him"""
        # Check if the user and guild to add the role is valid
        if payload.member is None or payload.guild_id is None:
            logger.warning("Missing data to add role in %s", __name__)
            return

        if (
            WELCOME_MESSAGES.get(payload.guild_id) is None
            or payload.message_id in WELCOME_MESSAGES[payload.guild_id]
        ):
            try:
                guild = next(guild for guild in self.bot.guilds if guild.id == payload.guild_id)
                member_role = discord.utils.get(guild.roles, name=OTTER_ROLE)
                if member_role is None:
                    logger.warning("Not role found in %s for guild %s", __name__, guild.name)
                    return
                await discord.Member.add_roles(payload.member, member_role)
            except StopIteration:
                logger.warning("Not guild found in %s", __name__)
            except discord.Forbidden:
                logger.error("Not permissions to add the role in %s", __name__)
            except discord.HTTPException:
                logger.error("Adding roles failed in %s", __name__)
            except Exception:
                logger.error("Exception in %s", __name__)


async def setup(bot: Bot) -> None:
    """Required setup method"""
    await bot.add_cog(BotEvents(bot, debug.Formatter))
