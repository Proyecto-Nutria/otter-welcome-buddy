from typing import Any

from otter_welcome_buddy.gql_service.gql_utils import get_deserialized_data
from otter_welcome_buddy.gql_service.leetcode_gql_conn import LeetcodeGqlConn
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeDailyChallengeModel
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeUserModel
from otter_welcome_buddy.gql_service.query.leetcode_queries import ACTIVE_DAILY_CHALLENGE_QUERY
from otter_welcome_buddy.gql_service.query.leetcode_queries import USER_PROFILE_QUERY


class GqlLeetcodeHandler:
    """Class to interact with the table role_config via static methods"""

    @staticmethod
    async def gen_user_public_profile(username: str) -> LeetcodeUserModel | None:
        """
        Fetches the public profile of a LeetCode user.

        Args:
            username (str): The username of the LeetCode user.

        Returns:
            LeetcodeUserModel | None: The deserialized user profile data if found, otherwise None.
        """
        variables: dict[str, Any] = {
            "username": username,
        }

        async with LeetcodeGqlConn() as gql_conn:
            response = await gql_conn.execute(USER_PROFILE_QUERY, variables)

        if response is None:
            return None
        return get_deserialized_data(LeetcodeUserModel, response["matchedUser"])

    @staticmethod
    async def gen_daily_challenge() -> LeetcodeDailyChallengeModel | None:
        """
        Fetches the daily challenge on Leetcode.

        Returns:
            LeetcodeDailyChallengeModel: The daily challenge data if found, otherwise None.
        """
        async with LeetcodeGqlConn() as gql_conn:
            response = await gql_conn.execute(ACTIVE_DAILY_CHALLENGE_QUERY)

        if response is None:
            return None
        return get_deserialized_data(
            LeetcodeDailyChallengeModel,
            response["activeDailyCodingChallengeQuestion"],
        )
