from mongoengine import DoesNotExist

from otter_welcome_buddy.database.models.external.user_model import UserModel


class DbUserHandler:
    """Class to interact with the table user via static methods"""

    @staticmethod
    def get_user(user_id: int, guild_id: int) -> UserModel | None:
        """Static method to get a user by its id"""
        try:
            user_model: UserModel = UserModel.objects(user_id=user_id, guild=guild_id).get()
            return user_model
        except DoesNotExist:
            return None

    @staticmethod
    def insert_user(user_model: UserModel) -> UserModel:
        """Static method to insert a user record"""
        user_model = user_model.save()
        return user_model

    @staticmethod
    def delete_user(user_id: int, guild_id: int) -> None:
        """Static method to delete an interview match record by a user_id"""
        user_model: UserModel | None = UserModel.objects(user_id=user_id, guild=guild_id).first()
        if user_model:
            user_model.delete()
