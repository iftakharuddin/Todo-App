import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """Base configuration."""

    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://test:test@localhost:5431/test"
    )
    SECRET_KEY = 'iftakhar'
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="very-important")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = os.getenv('REDIS_SERVER', 'redis')
    CACHE_REDIS_POST = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://"+CACHE_REDIS_HOST+":6379/0"
    CACHE_DEFAULT_TIMEOUT = 3300

    # Mail Settings
    MAIL_DEFAULT_SENDER = "noreply@flask.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = config("EMAIL_USER")
    MAIL_PASSWORD = config("EMAIL_PASSWORD")


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True