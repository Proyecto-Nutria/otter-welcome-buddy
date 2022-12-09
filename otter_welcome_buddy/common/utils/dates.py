from datetime import datetime


class DateUtils:
    """Utility class for datetime python library"""

    @staticmethod
    def get_current_month():
        return datetime.now().month
