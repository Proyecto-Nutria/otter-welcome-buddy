from mongoengine import DoesNotExist

from otter_welcome_buddy.database.models.external.leetcode_config_model import (
    LeetcodeConfigModel,
)


class DbLeetcodeConfigHandler:
    """Class to interact with the table leetcode_config via static methods"""

    @staticmethod
    def get_leetcode_config(
        guild_id: int,
    ) -> LeetcodeConfigModel | None:
        """Static method to get a leetcode config by its guild_id"""
        try:
            leetcode_config_model: LeetcodeConfigModel = LeetcodeConfigModel.objects(
                guild=guild_id,
            ).get()
            return leetcode_config_model
        except DoesNotExist:
            return None

    @staticmethod
    def get_all_leetcode_configs() -> list[LeetcodeConfigModel]:
        """Static method to get all the interview matches for a day"""
        leetcode_config_models: list[LeetcodeConfigModel] = list(
            LeetcodeConfigModel.objects(),
        )
        return leetcode_config_models

    @staticmethod
    def insert_leetcode_config(
        leetcode_config_model: LeetcodeConfigModel,
    ) -> LeetcodeConfigModel:
        """Static method to insert (or update) a leetcode config record"""
        leetcode_config_model = leetcode_config_model.save()
        return leetcode_config_model

    @staticmethod
    def delete_leetcode_config(guild_id: int) -> None:
        """Static method to delete a leetcode config record by a guild_id"""
        leetcode_config_model: LeetcodeConfigModel | None = LeetcodeConfigModel.objects(
            guild=guild_id,
        ).first()
        if leetcode_config_model:
            leetcode_config_model.delete()
