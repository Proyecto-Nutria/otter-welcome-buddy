"""An intent allows a bot to subscribe to specific buckets of events"""

from discord import Intents


def get_registered_intents() -> Intents:
    """Not registered intents cannot be used by the bot"""
    intents: Intents = Intents.default()
    intents.message_content = True
    intents.members = True
    return intents
