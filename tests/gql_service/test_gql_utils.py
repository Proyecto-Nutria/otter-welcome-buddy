import os
from typing import Any
from unittest import mock

import pytest
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import GraphQLError
from graphql import GraphQLSchema

from otter_welcome_buddy.gql_service.gql_utils import get_deserialized_data
from otter_welcome_buddy.gql_service.gql_utils import get_schema
from otter_welcome_buddy.gql_service.gql_utils import get_transport
from otter_welcome_buddy.gql_service.models.common import BaseGqlModel


def test_get_transport() -> None:
    url = "http://example.com/graphql"
    transport = get_transport(url)
    assert isinstance(transport, AIOHTTPTransport)
    assert transport.url == url


def test_get_schema_success() -> None:
    schema_filename = "test_schema.graphql"
    schema_content = """
    type Query {
        hello: String
    }
    """
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "schema",
        schema_filename,
    )

    with mock.patch("builtins.open", mock.mock_open(read_data=schema_content)):
        with mock.patch("os.path.join", return_value=schema_path):
            schema = get_schema(schema_filename)
            assert isinstance(schema, GraphQLSchema)


def test_get_schema_file_not_found() -> None:
    schema_filename = "non_existent_schema.graphql"
    with mock.patch("os.path.join", return_value="invalid_path"):
        with pytest.raises(FileNotFoundError):
            get_schema(schema_filename)


def test_get_schema_io_error() -> None:
    schema_filename = "test_schema.graphql"
    with mock.patch("builtins.open", mock.mock_open()) as mocked_open:
        mocked_open.side_effect = IOError
        with pytest.raises(IOError):
            get_schema(schema_filename)


def test_get_schema_graphql_error() -> None:
    schema_filename = "test_schema.graphql"
    invalid_schema_content = """
    type Query {
        hello: String
    """
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "schema",
        schema_filename,
    )

    with mock.patch("builtins.open", mock.mock_open(read_data=invalid_schema_content)):
        with mock.patch("os.path.join", return_value=schema_path):
            with pytest.raises(GraphQLError):
                get_schema(schema_filename)


def test_get_deserialized_data_success() -> None:
    class MockModel(BaseGqlModel):
        field_one: str | None = None

    data: dict[str, Any] = {"fieldOne": "value"}

    result = get_deserialized_data(MockModel, data)
    assert isinstance(result, MockModel)
    assert result.field_one == "value"


def test_get_deserialized_data_type_error() -> None:
    class MockModel:
        field_one: str | None = None

    data: dict[str, Any] = {"fieldOne": "value"}

    with pytest.raises(TypeError, match="Model is not inheriting from BaseGqlModel"):
        get_deserialized_data(MockModel, data)
