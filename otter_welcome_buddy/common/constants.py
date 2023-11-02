from enum import Enum


class CronExpressions(Enum):
    """Defined Cron Expressions"""

    DAY_ONE_OF_EACH_MONTH_CRON: str = "0 0 1 * *"
    NON_ENGLISH_TEACHERS_MESSAGE_TIME: str = "0 13 * * 2"  # 12:00 PM Pacific Time


COMMAND_PREFIX: str = "!"
