import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configurations."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-fallback-key-for-dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-SQLAlchemy 3+ relative sqlite URI resolves relative to instance path,
    # so sqlite:///database.db places it in instance/database.db.
    # We will use this behavior or support absolute path if specified in DATABASE_URL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

class DevelopmentConfig(Config):
    """Development configurations."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configurations."""
    DEBUG = False
    
    # Production must have a SECRET_KEY set in environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
