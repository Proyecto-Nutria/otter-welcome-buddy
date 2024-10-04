import os
from typing import Any
from typing import TypeVar

from gql.transport.aiohttp import AIOHTTPTransport
from graphql import build_ast_schema
from graphql import GraphQLSchema
from graphql import parse

from otter_welcome_buddy.gql_service.models.common import BaseGqlModel

T = TypeVar("T")

_SCHEMA_FOLDER_PATH: str = "schema"


def get_transport(url: str) -> AIOHTTPTransport:
    """
    Creates and returns an AIOHTTPTransport instance with the specified URL.

    Args:
        url (str): The URL to be used for the AIOHTTPTransport.

    Returns:
        AIOHTTPTransport: An instance of AIOHTTPTransport configured with the given URL.
    """
    return AIOHTTPTransport(url=url)


def get_schema(schema_filename: str) -> GraphQLSchema:
    """
    Loads and parses a GraphQL schema from a specified file.

    Args:
        schema_filename (str): The name of the schema file to load.

    Returns:
        GraphQLSchema: The parsed GraphQL schema object.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        IOError: If there is an error reading the schema file.
        GraphQLError: If there is an error parsing the schema.
    """
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        _SCHEMA_FOLDER_PATH,
        schema_filename,
    )
    with open(schema_path, encoding="utf-8") as source:
        document = parse(source.read())
        return build_ast_schema(document)


def get_deserialized_data(model: type[T], data: dict[str, Any]) -> T:
    """
    Deserialize the given data into an instance of the specified model type.

    Args:
        model (type[T]): The model class to deserialize the data into.
        data (dict[str, Any]): The data to be deserialized.

    Returns:
        T: An instance of the specified model type with the deserialized data.

    Raises:
        TypeError: If the deserialized data is not an instance of the specified model type.
    """
    if not issubclass(model, BaseGqlModel):
        raise TypeError("Model is not inheriting from BaseGqlModel")
    return model(**data)
