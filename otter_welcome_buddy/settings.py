import os

from dotenv import load_dotenv

load_dotenv()

BOT_TIMEZONE: str = "America/Mexico_City"
SUDO_CHANNEL_ID: int = int(os.environ["SUDO_CHANNEL_ID"])
