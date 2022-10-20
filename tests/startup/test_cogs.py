from unittest.mock import AsyncMock

import pytest

from otter_welcome_buddy.startup import cogs


def test_formatModulePath_cogExtensionFormat():
    # Arrange
    cog_path = cogs.new_user_joins.__file__

    # Act
    format_path = cogs.__format_module_path_into_cog_extension(cog_path)

    # Assert
    assert format_path == "cogs.new_user_joins"


@pytest.mark.asyncio
async def test_async_func_clone():
    # Arrange
    mock_thing = AsyncMock()
    mock_thing.load_extension = AsyncMock()

    # Act
    await cogs.register_cogs(mock_thing)

    # Assert
    assert mock_thing.load_extension.call_count == 1
