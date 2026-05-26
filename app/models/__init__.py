from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy extension object
db = SQLAlchemy()

# Import the models to make them available under app.models namespace
# Using relative imports to prevent circular dependency issues
from .user import User
from .log import PoopLog
from .suggestion import DietSuggestion

__all__ = ['db', 'User', 'PoopLog', 'DietSuggestion']
