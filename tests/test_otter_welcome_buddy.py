from otter_welcome_buddy import __version__
from otter_welcome_buddy.startup import intents


def test_version():
    assert __version__ == "0.1.0"


def test_getRegisteredIntents_returnMessageNMembers():
    registered_intents = intents.get_registered_intents()
    assert registered_intents.messages is True
    assert registered_intents.members is True
