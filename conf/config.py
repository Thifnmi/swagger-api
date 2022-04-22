import os
import json
from dotenv import load_dotenv
from decimal import Decimal

# load all environment from .env file. it 'll overwrite to use env
# variable directly from os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "..", ".env"))


def _get_config_value(key, default_value=None):
    value = os.environ.get(key, default_value)
    if (value is not None and value != "") and isinstance(value, str):
        if value.isdigit():
            value = int(value)
        elif isinstance(value, str) and key.endswith("LIST"):
            value = json.loads(value)

    return value


class BaseConfig(object):
    """..."""

    APP_NAME = _get_config_value("APP_NAME", "event-hook-service")
    DATABASE_URI = _get_config_value(
        "DATABASE_URL",
        "",
    )
    USE_LOG_FILE = eval(_get_config_value("USE_LOG_FILE", "False"))
    HOST = _get_config_value("HOST", "0.0.0.0")
    PORT = _get_config_value("PORT", 9997)
    SENTRY_DSN = _get_config_value("SENTRY_DSN", "")
    JSON_SORT_KEYS = _get_config_value("JSON_SORT_KEYS", "False")

    SENTRY_DSN = _get_config_value(
        "SENTRY_DSN",
        "",
    )


class DevelopmentConfig(BaseConfig):
    """..."""

    ENV = "development"

    pass


class StagingConfig(BaseConfig):
    """..."""

    ENV = "staging"

    pass


class ProductionConfig(BaseConfig):
    """..."""

    ENV = "production"

    pass


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "staging": StagingConfig,
}
