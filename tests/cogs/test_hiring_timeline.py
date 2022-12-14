from unittest.mock import AsyncMock, MagicMock

import pytest

from otter_welcome_buddy.cogs import hiring_timelines


@pytest.mark.asyncio
async def test_register_cog(mock_bot):
    # Arrange
    mock_bot.add_cog = AsyncMock()

    # Act
    await hiring_timelines.setup(mock_bot)

    # Assert
    assert mock_bot.add_cog.called


def test_call_formatter(mock_bot):
    # Arrange
    mock_timeline_fmt = MagicMock()
    mock_timeline_fmt.get_hiring_events_for = MagicMock()
    sut = hiring_timelines.Timelines(mock_bot, mock_timeline_fmt)

    # Act
    sut._get_hiring_events()

    # Assert
    assert mock_timeline_fmt.get_hiring_events_for.called
