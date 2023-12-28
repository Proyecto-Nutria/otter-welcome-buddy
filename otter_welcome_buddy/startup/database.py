import os

from discord.ext.commands import Bot
from dotenv import load_dotenv
from mongoengine import connect as mongo_connect
from pymongo import monitoring

from otter_welcome_buddy.common.constants import DATA_FILE_PATH
from otter_welcome_buddy.common.handlers.leetcode import LeetcodeAPI
from otter_welcome_buddy.common.utils.database import get_cache_engine
from otter_welcome_buddy.common.utils.types.handlers import ProblemsetListType
from otter_welcome_buddy.database.db_leetcode_problem import DbLeetcodeProblem
from otter_welcome_buddy.database.dbconn import BaseModel
from otter_welcome_buddy.database.handlers.db_guild_handler import DbGuildHandler
from otter_welcome_buddy.database.models.external.guild_model import GuildModel
from otter_welcome_buddy.log.dblogger import DbCommandLogger
from otter_welcome_buddy.database.dbconn import session_scope
from otter_welcome_buddy.database.models.leetcode_model import LeetcodeProblemModel


def init_guild_table(bot: Bot) -> None:
    """Verify that all the guilds that the bot is part of are in the database"""
    for guild in bot.guilds:
        if DbGuildHandler.get_guild(guild_id=guild.id) is None:
            guild_model: GuildModel = GuildModel(guild_id=guild.id)
            DbGuildHandler.insert_guild(guild_model=guild_model)


def _update_leetcode_problems() -> None:
    """Update the leetcode problems in the database to be used as cache"""
    leetcode_client: LeetcodeAPI = LeetcodeAPI()
    problemset_list: ProblemsetListType | None = leetcode_client.get_problemset_list()
    if problemset_list is None:
        print("No problems fetched from Leetcode")
        return
    with session_scope() as session:
        for problem in problemset_list.questions:
            leetcode_problem_model: LeetcodeProblemModel = LeetcodeProblemModel(
                question_slug=problem.titleSlug,
                title=problem.title,
                question_id=int(problem.questionId),
                frontend_id=int(problem.questionFrontendId),
                difficulty=problem.difficulty,
            )
            DbLeetcodeProblem.insert_leetcode_problem(
                session=session,
                leetcode_problem_model=leetcode_problem_model,
            )


async def init_database() -> None:
    """Initialize the database from the existing models"""
    load_dotenv()

    # Initialize local database used as cache - Sqlite3
    engine = get_cache_engine(db_path=DATA_FILE_PATH)
    BaseModel.metadata.create_all(engine)

    # Connect to global database - MongoDB
    monitoring.register(DbCommandLogger())
    mongo_connect(host=os.environ["MONGO_URI"])

    _update_leetcode_problems()
