from collections.abc import Generator
from unittest import mock

import pytest
from gql import Client
from gql.client import AsyncClientSession
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import GraphQLError
from graphql import GraphQLSchema
from pytest_mock import MockFixture

from otter_welcome_buddy.gql_service import base_gql_conn
from otter_welcome_buddy.gql_service.base_gql_conn import BaseGqlConn


class TestBaseGqlConn(BaseGqlConn):
    _GRAPHQL_URL = "http://example.com/graphql"
    _SCHEMA_FILENAME = "schema.graphql"


@pytest.fixture
def mock_transport(mocker: MockFixture) -> mock.Mock:
    transport = mock.Mock(spec=AIOHTTPTransport)
    return mocker.patch.object(
        base_gql_conn,
        "get_transport",
        return_value=transport,
    )


@pytest.fixture
def mock_schema(mocker: MockFixture) -> mock.Mock:
    schema = mock.Mock(spec=GraphQLSchema)
    return mocker.patch.object(
        base_gql_conn,
        "get_schema",
        return_value=schema,
    )


@pytest.fixture
def mock_client() -> Generator[tuple[mock.Mock, mock.Mock], None, None]:
    with mock.patch(
        "gql.Client.__aenter__",
        return_value=mock.AsyncMock(spec=AsyncClientSession),
    ) as mock_client_enter:
        with mock.patch("gql.Client.__aexit__", return_value=mock.AsyncMock()) as mock_client_exit:
            yield mock_client_enter, mock_client_exit


@pytest.mark.asyncio
async def test_context_manager(
    mock_transport: mock.Mock,
    mock_schema: mock.Mock,
    mock_client: tuple[mock.Mock, mock.Mock],
) -> None:
    async with TestBaseGqlConn() as conn:
        assert isinstance(conn._client, Client)  # noqa: SLF001
        assert isinstance(conn._session, AsyncClientSession)  # noqa: SLF001
        mock_schema.assert_called_once()
        mock_transport.assert_called_once()
        mock_client[0].assert_called_once()
        mock_client[1].assert_not_called()

    mock_client[0].assert_called_once()
    mock_client[1].assert_called_once()


@pytest.mark.asyncio
async def test_execute_success(
    mock_transport: mock.Mock,
    mock_schema: mock.Mock,
    mock_client: tuple[mock.Mock, mock.Mock],
) -> None:
    mock_session = mock.AsyncMock()
    mock_session.execute.return_value = {"data": "test"}
    mock_client[0].return_value = mock_session

    async with TestBaseGqlConn() as conn:
        result = await conn.execute("query { test }")
        assert result == {"data": "test"}


@pytest.mark.asyncio
async def test_execute_graphql_error(
    mock_transport: mock.Mock,
    mock_schema: mock.Mock,
    mock_client: tuple[mock.Mock, mock.Mock],
) -> None:
    mock_transport.return_value = mock.Mock()
    mock_schema.return_value = mock.Mock()
    mock_session = mock.AsyncMock()
    mock_session.execute.side_effect = GraphQLError("Test error")
    mock_client[0].return_value = mock_session

    async with TestBaseGqlConn() as conn:
        result = await conn.execute("query { test }")
        assert result is None


@pytest.mark.asyncio
async def test_execute_general_exception(
    mock_transport: mock.Mock,
    mock_schema: mock.Mock,
    mock_client: tuple[mock.Mock, mock.Mock],
) -> None:
    mock_transport.return_value = mock.Mock()
    mock_schema.return_value = mock.Mock()
    mock_session = mock.AsyncMock()
    mock_session.execute.side_effect = Exception("Test exception")
    mock_client[0].return_value = mock_session

    async with TestBaseGqlConn() as conn:
        result = await conn.execute("query { test }")
        assert result is None


@pytest.mark.asyncio
async def test_no_url_property() -> None:
    with pytest.raises(NotImplementedError):

        class MalformedTestGqlConn(BaseGqlConn):
            _GRAPHQL_URL = "http://example.com/graphql"


@pytest.mark.asyncio
async def test_no_schema_property() -> None:
    with pytest.raises(NotImplementedError):

        class MalformedTestGqlConn(BaseGqlConn):
            _SCHEMA_FILENAME = "schema.graphql"
