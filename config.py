import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os
import sys

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent  # .parent

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s",
    "%Y-%m-%d %H:%M:%S"
    )
LOG_DIR = PACKAGE_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'api.log'


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger


class Config:
    # DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # SECRET_KEY = 'this-really-needs-to-be-changed'
    SERVER_PORT = 5000
    PROPAGATE_EXCEPTIONS = True  # otherwise, test_item_no_auth - AssertionError: 401 != 500
    # 500 is Flask's internal server error, so that any unhandled exceptions do not give client any system info

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://alex:@localhost:5432/store_db'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # in current session of the terminal, run $ export SECRET_KEY='abcd'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY').encode()
    # SECRET_KEY = os.environ.get('SECRET_KEY').encode()

class ProductionConfig(Config):
    DEBUG = False
    SERVER_PORT = os.environ.get('PORT', 5000)
    # SERVER_ADDRESS: os.environ.get('SERVER_ADDRESS', '0.0.0.0')
    # SERVER_PORT: os.environ.get('SERVER_PORT', '5000')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False  # Otherwise: Error: A setup function was called after the first request was handled
    # the following config param is by default True when DEBUG is True
    # PROPAGATE_EXCEPTIONS = True  # otherwise, test_item_no_auth - AssertionError: 401 != 500
    # 500 is Flask's internal server error, so that any unhandled exceptions do not give client any system info
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # 'postgresql://postgres:1234@localhost:5432/test'
