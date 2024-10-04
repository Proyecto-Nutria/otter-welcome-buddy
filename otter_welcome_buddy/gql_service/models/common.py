from enum import Enum

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class BaseGqlModel(BaseModel):
    """
    BaseGqlModel is a base class for GraphQL models.

    This class serves as a foundation for other GraphQL models, mainly used for typing reasons.
    """

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


class AutoEnum(Enum):
    """
    AutoEnum is a subclass of Enum that automatically generates values for its members.

    Methods:
        _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
            Determines the value for an auto() call. This method is called by the Enum machinery
            to generate the next value for an enumeration member. It returns the name of the member
            as its value.
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        """Determines the value for an auto() call."""
        return name
