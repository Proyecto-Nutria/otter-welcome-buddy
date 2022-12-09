class Formatter:
    """Timeline messages"""

    @staticmethod
    def get_hiring_events_for(month: int):
        applicatons_opened_for = "Internship application opened for:"
        summer_season = "Summer Internships 🏝️"
        fall_season = "Fall Internships 🍂"
        winter_season = "Wintern Internships ⛄"

        match month:
            # Large Companies hire from August to January
            case 10, 11, 12, 1:
                return f"{applicatons_opened_for} {summer_season}"
            case 4, 5:
                return f"{applicatons_opened_for} {fall_season}"
            case 8, 9:
                return f"{applicatons_opened_for} {summer_season} {winter_season}"
