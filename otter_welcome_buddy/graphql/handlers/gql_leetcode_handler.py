from typing import Any

from otter_welcome_buddy.graphql.query.leetcode_queries import ACTIVE_DAILY_CHALLENGE_QUERY
from otter_welcome_buddy.graphql.query.leetcode_queries import USER_PROFILE_QUERY
from otter_welcome_buddy.graphql.services.leetcode_gql import LeetcodeGqlConn


class GqlLeetcodeHandler:
    """Class to interact with the table role_config via static methods"""

    @staticmethod
    async def gen_user_public_profile(username: str) -> dict[str, Any] | None:
        """
        Fetches the public profile of a LeetCode user.

        Args:
            username (str): The username of the LeetCode user.

        Returns:
            dict[str, Any]: The user profile data if found, otherwise None.
        """
        variables: dict[str, Any] = {
            "username": username,
        }

        async with LeetcodeGqlConn() as gql_conn:
            response = await gql_conn.execute(USER_PROFILE_QUERY, variables)

        if response is None:
            return None
        matched_user: dict[str, Any] | None = response.get("matchedUser")
        return matched_user

    @staticmethod
    async def gen_daily_challenge() -> dict[str, Any] | None:
        """
        Fetches the daily challenge on Leetcode.

        Returns:
            dict[str, Any]: The daily challenge data if found, otherwise None.
        """
        async with LeetcodeGqlConn() as gql_conn:
            response = await gql_conn.execute(ACTIVE_DAILY_CHALLENGE_QUERY)

        if response is None:
            return None
        daily_challenge: dict[str, Any] | None = response.get("activeDailyCodingChallengeQuestion")
        return daily_challenge
