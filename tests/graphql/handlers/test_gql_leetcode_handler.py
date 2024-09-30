from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from otter_welcome_buddy.graphql.handlers.gql_leetcode_handler import GqlLeetcodeHandler
from otter_welcome_buddy.graphql.query.leetcode_queries import ACTIVE_DAILY_CHALLENGE_QUERY
from otter_welcome_buddy.graphql.query.leetcode_queries import USER_PROFILE_QUERY
from otter_welcome_buddy.graphql.services.leetcode_gql import LeetcodeGqlConn

_USERNAME = "test_user"


@pytest.mark.asyncio
async def test_gen_user_public_profile_success() -> None:
    mocked_response = {"matchedUser": {"username": _USERNAME, "profile": {"ranking": 1}}}
    expected_response = {"username": _USERNAME, "profile": {"ranking": 1}}

    with patch.object(LeetcodeGqlConn, "execute", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mocked_response

        result = await GqlLeetcodeHandler.gen_user_public_profile(_USERNAME)

        mock_execute.assert_called_once_with(USER_PROFILE_QUERY, {"username": _USERNAME})
        assert result == expected_response


@pytest.mark.asyncio
async def test_gen_user_public_profile_not_found() -> None:
    expected_response = None

    with patch.object(LeetcodeGqlConn, "execute", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = expected_response

        result = await GqlLeetcodeHandler.gen_user_public_profile(_USERNAME)

        mock_execute.assert_called_once_with(USER_PROFILE_QUERY, {"username": _USERNAME})
        assert result == expected_response


@pytest.mark.asyncio
async def test_gen_daily_challenge_success() -> None:
    mocked_response = {
        "activeDailyCodingChallengeQuestion": {
            "date": "2024-09-30",
            "link": "/problems/design-a-stack-with-increment-operation/",
            "question": {
                "title": "Design a Stack With Increment Operation",
                "difficulty": "Medium",
                "topicTags": [{"name": "Array"}, {"name": "Stack"}, {"name": "Design"}],
            },
        },
    }
    expected_response = {
        "date": "2024-09-30",
        "link": "/problems/design-a-stack-with-increment-operation/",
        "question": {
            "title": "Design a Stack With Increment Operation",
            "difficulty": "Medium",
            "topicTags": [{"name": "Array"}, {"name": "Stack"}, {"name": "Design"}],
        },
    }

    with patch.object(LeetcodeGqlConn, "execute", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mocked_response

        result = await GqlLeetcodeHandler.gen_daily_challenge()

        mock_execute.assert_called_once_with(ACTIVE_DAILY_CHALLENGE_QUERY)
        assert result == expected_response


@pytest.mark.asyncio
async def test_gen_daily_challenge_not_found() -> None:
    expected_response = None

    with patch.object(LeetcodeGqlConn, "execute", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = expected_response

        result = await GqlLeetcodeHandler.gen_daily_challenge()

        mock_execute.assert_called_once_with(ACTIVE_DAILY_CHALLENGE_QUERY)
        assert result == expected_response
