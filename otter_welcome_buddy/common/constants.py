import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class CronExpressions(Enum):
    """Defined Cron Expressions"""

    DAY_ONE_OF_EACH_MONTH_CRON: str = "0 0 1 * *"


COMMAND_PREFIX: str = "!"

WELCOME_MESSAGES = os.environ.get("WELCOME_MESSAGES", "").split(",")

# Discord role that give access to admin role based commands
OTTER_ADMIN = "ROOT"
# Discord role that give access to moderator role based commands
OTTER_MODERATOR = "Collaborator"
# Discord role that give access to the remaining channels and is given when reacted to WELCOME_MESSAGES
OTTER_ROLE = "Interviewee"
