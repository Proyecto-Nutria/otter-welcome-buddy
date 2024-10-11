from otter_welcome_buddy.gql_service.base_gql_conn import BaseGqlConn


class LeetcodeGqlConn(BaseGqlConn):
    """
    LeetcodeGqlConn is a class that manages the connection to the LeetCode GraphQL API.

    Attributes:
        _GRAPHQL_URL (str): The URL endpoint for the LeetCode GraphQL API.
        _SCHEMA_FILENAME (str): The filename of the GraphQL schema used for the connection.
    """

    _GRAPHQL_URL: str = "https://leetcode.com/graphql/"
    _SCHEMA_FILENAME: str = "leetcode.gql"
