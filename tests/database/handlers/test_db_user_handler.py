import pytest
from mongoengine import DoesNotExist
from mongoengine import ValidationError
from mongomock import MongoClient

from otter_welcome_buddy.database.handlers.db_user_handler import DbUserHandler
from otter_welcome_buddy.database.models.external.guild_model import GuildModel
from otter_welcome_buddy.database.models.external.user_model import UserModel


def test_get_user_succeed(
    temporary_mongo_connection: MongoClient,
    mock_guild_model: GuildModel,
) -> None:
    # Arrange
    mocked_user_id: int = 123
    mocked_user_model: UserModel = UserModel(
        user_id=mocked_user_id,
        guild=mock_guild_model,
    )
    mocked_user_model.save()

    # Act
    result = DbUserHandler.get_user(user_id=mocked_user_id, guild_id=mock_guild_model.id)

    # Assert
    assert result is not None
    assert result.user_id == mocked_user_id
    assert result.guild.id == mock_guild_model.id


def test_get_user_not_found(temporary_mongo_connection: MongoClient) -> None:
    # Act
    result = DbUserHandler.get_user(user_id=123, guild_id=123)

    # Assert
    assert result is None


def test_insert_user_succeed(
    temporary_mongo_connection: MongoClient,
    mock_guild_model: GuildModel,
) -> None:
    # Arrange
    mocked_user_id: int = 123
    mocked_user_model: UserModel = UserModel(
        user_id=mocked_user_id,
        guild=mock_guild_model,
    )

    # Act
    result = DbUserHandler.insert_user(user_model=mocked_user_model)

    # Assert
    assert result is not None
    assert result.user_id == mocked_user_id
    assert result.guild.id == mock_guild_model.id


def test_insert_user_failed(temporary_mongo_connection: MongoClient) -> None:
    # Arrange
    mocked_user_model: UserModel = UserModel()

    # Act / Assert
    with pytest.raises(ValidationError):
        DbUserHandler.insert_user(user_model=mocked_user_model)


def test_delete_user_valid_id(
    temporary_mongo_connection: MongoClient,
    mock_guild_model: GuildModel,
) -> None:
    # Arrange
    mocked_user_id: int = 123
    mocked_user_model: UserModel = UserModel(
        user_id=mocked_user_id,
        guild=mock_guild_model,
    )
    mocked_user_model.save()

    # Act
    DbUserHandler.delete_user(user_id=mocked_user_id, guild_id=mock_guild_model.id)

    # Assert
    with pytest.raises(DoesNotExist):
        UserModel.objects(user_id=mocked_user_id, guild=mock_guild_model.id).get()


def test_delete_user_invalid_id(temporary_mongo_connection: MongoClient) -> None:
    # Act
    DbUserHandler.delete_user(user_id=123, guild_id=123)

    # Assert
    with pytest.raises(DoesNotExist):
        UserModel.objects(user_id=123, guild=123).get()
