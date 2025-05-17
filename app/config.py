import logging
import sys

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

from app.logger import InterceptHandler

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)


def get_config_secret(key: str, default: str = "") -> Secret:
    """Type-safe secret configuration loader"""
    value = config(key, default=default)
    return Secret(str(value))


SECRET_KEY: Secret = get_config_secret("SECRET_KEY")

PROJECT_NAME: str = config("PROJECT_NAME", default="TestMart")

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
