from mongoengine import Document
from mongoengine import IntField


class UserModel(Document):
    """
    A model that represents a user in the database.

    Attributes:
        user_id (int):  The identifier for the user, is taken from discord records and is
                        the primary key of the object
    """

    user_id = IntField(primary_key=True, required=True)
