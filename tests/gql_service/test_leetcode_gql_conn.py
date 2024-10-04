from otter_welcome_buddy.gql_service.leetcode_gql_conn import LeetcodeGqlConn


def test_graphql_url() -> None:
    assert LeetcodeGqlConn._GRAPHQL_URL == "https://leetcode.com/graphql/"  # pylint: disable=W0212


def test_schema_filename() -> None:
    assert LeetcodeGqlConn._SCHEMA_FILENAME == "leetcode.gql"  # pylint: disable=W0212
