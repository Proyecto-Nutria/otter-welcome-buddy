import os

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from otter_welcome_buddy.common.utils.discord_ import insert_company
from otter_welcome_buddy.google_spreadsheet.validation import validate_credentials

load_dotenv()


class SheetManager:
    """Handles all the sheets actions"""

    def __init__(self, sheet_id: str = os.environ["SHEET_ID"]) -> None:
        self.sheet_id: str = sheet_id
        self.creds: Credentials = validate_credentials()

    def query(self, query_range: str) -> list:
        """
        Make a request to the spreadsheet API.
        Returns a list with the information inside of the query_range argument.
        """
        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(
                    spreadsheetId=self.sheet_id,
                    range=query_range,
                )
                .execute()
            )
            values: list = result.get("values", [])

            return values

        except HttpError as err:
            print(err)
        return []

    def get_allowed_companies(self) -> list:
        """
        Get information from the 'Allowed Companies' sheet.
        Returns a list with the information in the sheet.
        """
        try:
            # Build the service and make the API request
            service = build("sheets", "v4", credentials=self.creds)
            sheet = service.spreadsheets()
            result = (
                sheet.values().get(spreadsheetId=self.sheet_id, range="Allowed Companies").execute()
            )
            values: list = result.get("values", [])

            return values

        except HttpError as err:
            print(err)
            return []

    def insert_data(
        self,
        user: str,
        company: str,
        index_to_insert: int = 0,
        column: str = "A",
    ) -> str:
        """
        Helper function to insert data into the Google SpreadSheet
        """

        # Return numbers will be explained in 'message_handler' function

        # Get all the information from the SpreadSheet
        service = build("sheets", "v4", credentials=self.creds).spreadsheets()
        response = service.values().get(spreadsheetId=self.sheet_id, range="A:I").execute()
        rows = response.get("values", [])

        # Iterate over all the rows
        # check if there's a process with this 'user' and 'company'
        for index, row in enumerate(rows):
            # If there's already a process with the 'user' and 'company'
            # We want to know if it's a valid process
            if len(row) >= 2 and row[0] == user and row[1] == company:
                # For loop to check it there's is an advanced process
                # 'index_to_insert' is from where we want to insert our check
                # We iterate just all the way before 'offer' and 'rejection'
                for i in range(index_to_insert, len(row) - 2):
                    # 'user' already applied to this 'company'
                    if row[i] != "-" and index_to_insert == 2:
                        return "0"

                    # There's an advanced process with this 'user' and 'company'
                    if row[i] != "-":
                        return "1"

                # A desition has ben made by the company (either rejection or offer)
                if row[len(row) - 2] != "-" or row[len(row) - 1] != "-":
                    return "2"

                # If we already iterated over the row
                # And we didn't find any advanced process, we check the 'index_to_insert'

                service.values().update(
                    spreadsheetId=self.sheet_id,
                    range=f"{column}{index + 1}",
                    valueInputOption="RAW",
                    body={"values": [["✅"]]},
                ).execute()
                return "3"

        # Already checked all rows and there's no process with 'user' and 'company'
        # A process starts with 'user' and 'company'
        # We mark all positions with a '-' for better error control
        if index_to_insert == 2:
            values = [[user, company, "✅", "-", "-", "-", "-", "-", "-"]]
            next_row = len(rows) + 1

            service.values().append(
                spreadsheetId=self.sheet_id,
                range=f"A{next_row}:I{next_row}",
                valueInputOption="RAW",
                body={"values": values},
            ).execute()
            return "4"

        # 'user' has not applied to 'company' yet

        return "5"

    def insert_company_data(self, company: str) -> bool:
        """
        Insert company name into the Allowed Companies sheet
        """
        response = insert_company(company, self.creds, self.sheet_id)
        return response

    def insert_apply_data(self, user: str, company: str) -> str:
        """
        Insert application data into the Google SpreadSheet (Apply column).
        """
        response = self.insert_data(user, company, 2)
        return response

    def insert_oa_data(self, user: str, company: str) -> str:
        """
        Insert online assessment data into the Google SpreadSheet (Online Assessment column).
        """
        response = self.insert_data(user, company, 3, "D")
        return response

    def insert_phone_data(self, user: str, company: str) -> str:
        """
        Insert phone interview data into the Google SpreadSheet (Phone column).
        """
        response = self.insert_data(user, company, 4, "E")
        return response

    def insert_interview_data(self, user: str, company: str) -> str:
        """
        Insert interview data into the Google SpreadSheet (Interview column).
        """
        response = self.insert_data(user, company, 5, "F")
        return response

    def insert_finalround_data(self, user: str, company: str) -> str:
        """
        Insert final round Interview data into the Google SpreadSheet (Final Round column).
        """
        response = self.insert_data(user, company, 6, "G")
        return response

    def insert_offer_data(self, user: str, company: str) -> str:
        """
        Insert offer data into the Google SpreadSheet (Offer column).
        """
        response = self.insert_data(user, company, 7, "H")
        return response

    def insert_rejection_data(self, user: str, company: str) -> str:
        """
        Insert rejection data into the Google SpreadSheet (Rejection column).
        """
        response = self.insert_data(user, company, 8, "I")
        return response
