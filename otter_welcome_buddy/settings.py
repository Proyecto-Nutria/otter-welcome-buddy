import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()


WELCOME_MESSAGES = getenv("WELCOME_MESSAGES", "").split(",")
TIME_ZONE: str = "America/Mexico_City"
ENGLISH_CHANNEL_ID: int = int(os.environ["GENERAL_CHANNEL_ID"])
NON_ENGLISH_TEACHERS_CHANNEL_ID: int = int(os.environ["ROOT_CHANNEL_ID"])
