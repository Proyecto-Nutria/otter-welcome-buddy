import os

from gql.transport.aiohttp import AIOHTTPTransport
from graphql import build_ast_schema
from graphql import GraphQLSchema
from graphql import parse

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
