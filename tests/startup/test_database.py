from unittest.mock import MagicMock
from unittest.mock import patch

from pytest_mock import MockFixture

from otter_welcome_buddy.startup import database


@patch("otter_welcome_buddy.startup.database.BaseModel.metadata.create_all")
def test_initDatabase(mock_create_all: MagicMock, mocker: MockFixture):
    # Arrange
    mock_engine = MagicMock()

    mock_get_engine = mocker.patch(
        "otter_welcome_buddy.startup.database.get_engine",
        return_value=mock_engine,
    )

    # Act
    database.init_database()

    # Assert
    print(type(mock_create_all))
    mock_get_engine.assert_called_once()
    mock_create_all.assert_called_once_with(mock_engine)
