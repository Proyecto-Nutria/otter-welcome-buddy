import os
from enum import Enum


class CronExpressions(Enum):
    """Defined Cron Expressions"""

    DAY_ONE_OF_EACH_MONTH_CRON: str = "0 0 1 * *"
    WEDNESDAY_NOON_CRON: str = "0 12 * * 2"


class DiscordCommonRoles(Enum):
    """Common roles present by default in Discord"""

    EVERYONE: str = "@everyone"
    HERE: str = "@here"


COMMAND_PREFIX: str = "!"

DATA_DIR: str = "data"
DATA_FILE: str = "otter-buddy.db"
DATA_FILE_PATH: str = os.path.join(DATA_DIR, DATA_FILE)

ALL_DIRS = (
    attrib_value
    for attrib_name, attrib_value in list(globals().items())
    if attrib_name.endswith("DIR")
)

# Discord role that give access to admin role based commands
OTTER_ADMIN: str = "ROOT"
# Discord role that give access to moderator role based commands
OTTER_MODERATOR: str = "Collaborator"
# Discord role that give access to the remaining channels and is
# given when the user react to WELCOME_MESSAGES
OTTER_ROLE: str = "Interviewee"
# URL to the header image used for branding or visual identity in the Discord server
OTTER_HEADER_IMAGE: str = "https://shorturl.at/blqMV"
