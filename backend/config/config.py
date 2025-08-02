import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True
    
    # Database configuration (nếu cần)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration (nếu cần authentication)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # CORS configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']  # React dev servers
    
    # OpenAI configuration for conversation features
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '1500'))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))
    
    # OpenAI configuration for RAG features
    OPENAI_ENDPOINT = os.environ.get('OPENAI_ENDPOINT')
    OPENAI_API_KEY_EMBEDDING = os.environ.get('OPENAI_API_KEY_EMBEDDING')
    
    # Database paths for TinyDB
    CONVERSATIONS_DB = os.environ.get('CONVERSATIONS_DB', 'data/conversations.json')
    MESSAGES_DB = os.environ.get('MESSAGES_DB', 'data/messages.json')
    DATA_FILES_DB = os.environ.get('DATA_FILES_DB', 'data/data_files.json')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
