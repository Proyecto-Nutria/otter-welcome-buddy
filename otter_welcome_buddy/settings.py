import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()


BOT_TIMEZONE: str = "America/Mexico_City"
WELCOME_MESSAGES = getenv("WELCOME_MESSAGES", "").split(",")
ADMIN_ROLE_ID: str = os.environ["ADMIN_ROLE_ID"]
COLLABORATOR_ROLE_ID: str = os.environ["COLLABORATOR_ROLE_ID"]
ENGLISH_CHANNEL_ID: int = int(os.environ["GENERAL_CHANNEL_ID"])
NON_ENGLISH_TEACHERS_CHANNEL_ID: int = int(os.environ["ROOT_CHANNEL_ID"])
