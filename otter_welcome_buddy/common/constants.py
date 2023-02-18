import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class CronExpressions(Enum):
    """Defined Cron Expressions"""

    DAY_ONE_OF_EACH_MONTH_CRON: str = "0 0 1 * *"


COMMAND_PREFIX: str = "!"

WELCOME_MESSAGES = os.environ.get("WELCOME_MESSAGES", "").split(",")

OTTER_ADMIN = os.environ.get("OTTER_ADMIN", "Admin")
OTTER_MODERATOR = os.environ.get("OTTER_MODERATOR", "Moderator")
OTTER_ROLE = os.environ.get("OTTER_ROLE", "Member")
