import os

from dotenv import load_dotenv

load_dotenv()

BOT_TIMEZONE: str = "America/Mexico_City"
SUDO_CHANNEL_ID: int = int(os.environ["SUDO_CHANNEL_ID"])
TRACKER_CHANNEL_ID: int = int(os.environ["TRACKER_CHANNEL_ID"])
ADMIN_ROLE_ID: str = os.environ["ADMIN_ROLE_ID"]
COLLABORATOR_ROLE_ID: str = os.environ["COLLABORATOR_ROLE_ID"]
