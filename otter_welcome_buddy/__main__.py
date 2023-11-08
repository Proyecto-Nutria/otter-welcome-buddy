import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from multiprocessing import Queue

import logging_loki
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or
from dotenv import load_dotenv

from otter_welcome_buddy.cogs.roles import Roles
from otter_welcome_buddy.common.constants import ALL_DIRS
from otter_welcome_buddy.common.constants import COMMAND_PREFIX
from otter_welcome_buddy.common.constants import LOG_FILE_PATH
from otter_welcome_buddy.startup import cogs
from otter_welcome_buddy.startup import database
from otter_welcome_buddy.startup import intents


def _setup() -> None:
    # Load enviroment variables.
    load_dotenv()

    # Make required directories.
    for path in ALL_DIRS:
        os.makedirs(path, exist_ok=True)

    # Logging to console and file on daily interval
    logging_handlers: list[logging.Handler] = [
        logging.StreamHandler(),
        TimedRotatingFileHandler(
            LOG_FILE_PATH,
            when="D",
            backupCount=3,
            utc=True,
        ),
    ]

    grafana_loki_uri: str | None = os.environ.get("GRAFANA_LOKI_URI")
    if grafana_loki_uri:
        loki_handler = logging_loki.LokiQueueHandler(
            Queue(-1),
            url=grafana_loki_uri,
            tags={"application": "otter-welcome-buddy"},
            version="1",
        )
        logging_handlers.append(loki_handler)

    logging.basicConfig(
        format="{asctime}:{levelname}:{name}:{message}",
        style="{",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
        handlers=logging_handlers,
    )


async def main() -> None:
    """Principal function to be called by Docker"""
    _setup()

    bot: Bot = Bot(
        command_prefix=when_mentioned_or(COMMAND_PREFIX),
        intents=intents.get_registered_intents(),
    )

    async with bot:
        await database.init_database()
        Roles.init_welcome_messages()
        await cogs.register_cogs(bot)
        await bot.start(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
