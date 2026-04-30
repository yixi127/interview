from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .category import Category
from .question import Question

__all__ = ["db", "User", "Category", "Question"]
