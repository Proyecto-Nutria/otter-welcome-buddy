class Formatter:
    """Dependency to inject messages"""

    @staticmethod
    def non_english_club_message() -> str:
        """Message ask English session"""
        return "Hey yo, English club this week? "

    @staticmethod
    def english_club_message(hour: str) -> str:
        """Message when an English session has been scheduled"""
        message = f"""
        📣 Join us for an exciting English Club session next Sunday at {hour} Pacific Time! 🕗🌟

        🗓️ Mark your calendars and set a reminder to join us. Don't miss out on the chance

        to improve your language skills and connect with fellow language enthusiasts!

        See you there on the English Club channel! 🎭
        """

        return message
