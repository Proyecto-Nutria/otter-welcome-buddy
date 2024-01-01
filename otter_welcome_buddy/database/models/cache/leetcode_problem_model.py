from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from otter_welcome_buddy.database.dbconn import BaseModel


class LeetcodeProblemModel(BaseModel):
    """
    A model that represents a leetcode problem in the cache.

    Attributes:
        question_slug (str):    Primary key that identifies the problem in leetcode
        title (str):            Title that has the problem in leetcode
        question_id (int):      Identifier of the problem in leetcode
        frontend_id (int):      Identifier of the problem in leetcode frontend
        difficulty (str):       Difficulty of the problem, could be one of hard/medium/easy
    """

    __tablename__ = "leetcode_problem"

    question_slug = Column(String, primary_key=True)
    title = Column(String)
    question_id = Column(Integer)
    frontend_id = Column(Integer)
    difficulty = Column(String)
