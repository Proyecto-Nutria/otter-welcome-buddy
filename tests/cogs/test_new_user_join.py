from unittest.mock import AsyncMock, MagicMock

import pytest

from otter_welcome_buddy.cogs import new_user_joins


@pytest.fixture
def mock_bot():
    mock_bot = AsyncMock()
    return mock_bot


@pytest.fixture
def mock_msg_fmt():
    mock_msg_fmt = MagicMock()
    mock_msg_fmt.bot_is_ready = MagicMock()
    return mock_msg_fmt


@pytest.fixture
def mock_debug_fmt():
    mock_debug_fmt = MagicMock()
    mock_debug_fmt.welcome_message = MagicMock()
    return mock_debug_fmt


@pytest.mark.asyncio
async def test_cogSetup_registerCommand(mock_bot, mock_msg_fmt, mock_debug_fmt):
    # Arrange
    mock_bot.add_cog = AsyncMock()

    # Act
    await new_user_joins.setup(mock_bot)

    # Assert
    assert mock_bot.add_cog.called


@pytest.mark.asyncio
async def test_onReady_printMessage(mock_bot, mock_msg_fmt, mock_debug_fmt):
    # Arrange
    cog = new_user_joins.Greetings(mock_bot, mock_msg_fmt, mock_debug_fmt)

    # Act
    await cog.on_ready()

    # Assert
    assert mock_debug_fmt.bot_is_ready.called


@pytest.mark.asyncio
async def test_onMemberJoins_sendMessage(mock_bot, mock_msg_fmt, mock_debug_fmt):
    # Arrange
    mock_member = AsyncMock()
    cog = new_user_joins.Greetings(mock_bot, mock_msg_fmt, mock_debug_fmt)

    # Act
    await cog.on_member_join(mock_member)

    # Assert
    assert mock_msg_fmt.welcome_message.called


def test_commandMessage_correctMessage(mock_bot, mock_msg_fmt, mock_debug_fmt):
    # Act
    cog = new_user_joins.Greetings(mock_bot, mock_msg_fmt, mock_debug_fmt)
    cog._command_message()

    # Assert
    assert mock_msg_fmt.welcome_message.called
