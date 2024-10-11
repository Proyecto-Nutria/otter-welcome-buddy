from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from otter_welcome_buddy.gql_service.handlers.gql_leetcode_handler import GqlLeetcodeHandler
from otter_welcome_buddy.gql_service.leetcode_gql_conn import LeetcodeGqlConn
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeDailyChallengeModel
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeQuestionModel
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeTopicTagModel
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeUserModel
from otter_welcome_buddy.gql_service.models.gql_leetcode_model import LeetcodeUserProfileModel
from otter_welcome_buddy.gql_service.query.leetcode_queries import ACTIVE_DAILY_CHALLENGE_QUERY
from otter_welcome_buddy.gql_service.query.leetcode_queries import USER_PROFILE_QUERY

_USERNAME = "test_user"


@pytest.mark.asyncio
async def test_gen_user_public_profile_success() -> None:
    mocked_response = {"matchedUser": {"username": _USERNAME, "profile": {"ranking": 1}}}
    expected_response = LeetcodeUserModel(
        username=_USERNAME,
        profile=LeetcodeUserProfileModel(ranking=1),
    )

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
                "categoryTitle": "Algorithms",
                "topicTags": [{"name": "Array"}, {"name": "Stack"}, {"name": "Design"}],
            },
        },
    }
    expected_response = LeetcodeDailyChallengeModel(
        date="2024-09-30",
        link="/problems/design-a-stack-with-increment-operation/",
        question=LeetcodeQuestionModel(
            title="Design a Stack With Increment Operation",
            difficulty="Medium",
            category_title="Algorithms",
            topic_tags=[
                LeetcodeTopicTagModel(name="Array"),
                LeetcodeTopicTagModel(name="Stack"),
                LeetcodeTopicTagModel(name="Design"),
            ],
        ),
    )

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
