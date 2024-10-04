import logging
from abc import ABC
from abc import abstractmethod
from typing import Any

from gql import Client
from gql import gql
from gql.client import AsyncClientSession
from graphql import GraphQLError

from otter_welcome_buddy.gql_service.gql_utils import get_schema
from otter_welcome_buddy.gql_service.gql_utils import get_transport


logger = logging.getLogger(__name__)


class BaseGqlConn(ABC):
    """
    BaseGqlConn is an abstract base class that provides a context manager for establishing
    and managing a GraphQL client connection. It includes methods for executing GraphQL
    queries and handling errors.

    Attributes:
        _client (Client): The GraphQL client instance.
        _session (AsyncClientSession): The asynchronous client session.

    Abstract Properties:
        _GRAPHQL_URL (str): The URL of the GraphQL API used.
        _SCHEMA_FILENAME (str): The filename of the corresponding schema for the GraphQL API.

    Methods:
        __aenter__() -> "BaseGqlConn":
            Asynchronously enters the context manager, initializes the GraphQL client and session.

        __aexit__(exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
            Asynchronously exits the context manager, closes the GraphQL client session.

        execute(query_str: str, variables: dict[str, Any] | None = None) -> dict[str, Any] | None:
            Returns the response data as a dictionary. If the request fails,
            logs the error and returns None.

            query_str (str): The GraphQL query string.
            variables (dict[str, Any]): A dictionary of variables to include in the request.
    """

    _client: Client
    _session: AsyncClientSession

    @classmethod  # type: ignore
    @property
    @abstractmethod
    def _GRAPHQL_URL(cls) -> str:  # pylint: disable=C0103
        """Return the URL of the GraphQL API used"""
        raise NotImplementedError

    @classmethod  # type: ignore
    @property
    @abstractmethod
    def _SCHEMA_FILENAME(cls) -> str:  # pylint: disable=C0103
        """Return the filename of the corresponding schema for the GraphQL API"""
        raise NotImplementedError

    async def __aenter__(self) -> "BaseGqlConn":
        transport = get_transport(url=self._GRAPHQL_URL)
        schema = get_schema(schema_filename=self._SCHEMA_FILENAME)
        self._client = Client(transport=transport, schema=schema, fetch_schema_from_transport=False)
        self._session = await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def execute(
        self,
        query_str: str,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """
        Sends a GraphQL request to the service URL using the specified query and variables.
        Returns the response data as a dictionary. If the request fails, log the error and
        returns None.

        Parameters:
            query:          The GraphQL query string.
            variables:      A dictionary of variables to include in the request.

        Returns:
            dict[str, Any] | None: The response data as a dictionary, or None if the request fails.
        """
        try:
            query = gql(query_str)
            result: dict[str, Any] = await self._session.execute(query, variable_values=variables)
            return result
        except GraphQLError as ex:
            logger.exception(
                "A syntax error (%s) happened while analyzing the query: \n%s",
                ex,
                query_str,
            )
            return None
        except Exception as ex:
            logger.error("Exception %s in %s", ex, __name__)
            return None
