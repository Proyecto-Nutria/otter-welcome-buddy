class Formatter:
    """Timeline messages"""

    @staticmethod
    def get_hiring_events_for(month: int) -> str:
        """Internship application for whole year"""
        applicatons_opened_for = "Internship application opened for:"

        no_season = "Not this month, try next one 🦦"
        summer_season = "Summer Internships 🏝️"
        fall_season = "Fall Internships 🍂"
        winter_season = "Wintern Internships ⛄"

        print(month)

        match month:
            # Large Companies hire from August to January
            case 10 | 11 | 12 | 1:
                return f"{applicatons_opened_for} {summer_season}"
            case 4 | 5:
                return f"{applicatons_opened_for} {fall_season}"
            case 8 | 9:
                return f"{applicatons_opened_for} {winter_season}"
            case 2 | 3 | 6 | 7:
                return f"{applicatons_opened_for} {no_season}"
            case _:
                raise ValueError()
