from enum import Enum


class CronExpressions(Enum):
    """Defined Cron Expressions"""

    DAY_ONE_OF_EACH_MONTH_CRON: str = "0 0 1 * *"
    # ENGLISH_CLUB_TIME: str = "2 20 * * 4"
    ENGLISH_CLUB_TIME: str = "* * * * *"


COMMAND_PREFIX: str = "!"
