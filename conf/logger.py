"""
Usage example:
    from logger import get_logger
    log = get_logger()
    log.info('my_event', my_key1='val 1', my_key2=5, my_key3=[1, 2, 3], my_key4={'a': 1, 'b': 2})
List of metadata keys in each log message:
    event
    _func
    _level
    _levelno
    _lineno
    _module
    _thread_id
    _thread_name
    _time_unix
    _time_human_localized
    _time_human_utc
Requirements: pytz
Limitations: multithreading is supported but not multiprocessing.
"""

import collections
import datetime
import inspect
import logging
import logging.config
import os
import platform
import sys
import tempfile
import threading
import time
import structlog

from conf.config import config

import pytz
from structlog_sentry import SentryProcessor

env = os.getenv("ENV", "development")
BASE_LOGGER_NAME = config[env].APP_NAME
IS_CONFIGURED = False
LOGGED_TZ = pytz.timezone("Asia/Ho_Chi_Minh")
TEMPDIR = "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "()": logging.handlers.TimedRotatingFileHandler,
            "filename": os.path.join(
                os.getenv("LOGDIR", TEMPDIR), BASE_LOGGER_NAME + ".log"
            ),
            "when": "midnight",
            "backupCount": 14,
            "utc": True,
        },
    },
    "loggers": {
        BASE_LOGGER_NAME: {"propagate": False, "handlers": ["file"], "level": "DEBUG",},
    },
}


def _event_uppercase(
    logger, method_name, event_dict
):  # pylint: disable=unused-argument
    event_dict["event"] = event_dict["event"].upper()
    return event_dict


def _add_timestamp(logger, method_name, event_dict):  # pylint: disable=unused-argument
    event_dict["_time_unix"] = time.time()
    dt_utc = datetime.datetime.fromtimestamp(
        event_dict["_time_unix"], datetime.timezone.utc
    )
    event_dict["_time_human_utc"] = dt_utc.isoformat()
    event_dict["_time_human_localized"] = {
        LOGGED_TZ.zone: dt_utc.astimezone(LOGGED_TZ).isoformat()
    }
    return event_dict


def _add_caller_info(
    logger, method_name, event_dict
):  # pylint: disable=unused-argument
    # Typically skipped funcs: _add_caller_info, _process_event, _proxy_to_logger, _proxy_to_logger
    frame = inspect.currentframe()
    while frame:
        frame = frame.f_back
        module = frame.f_globals["__name__"]
        if module.startswith("structlog."):
            continue
        event_dict["_module"] = module
        event_dict["_lineno"] = frame.f_lineno
        event_dict["_func"] = frame.f_code.co_name
        return event_dict


def _add_log_level(logger, method_name, event_dict):  # pylint: disable=unused-argument
    event_dict["_level"] = method_name
    event_dict["_levelno"] = getattr(logging, method_name.upper())
    return event_dict


def _add_thread_info(
    logger, method_name, event_dict
):  # pylint: disable=unused-argument
    thread = threading.current_thread()
    event_dict["_thread_id"] = thread.ident
    event_dict["_thread_name"] = thread.name
    return event_dict


def _order_keys(logger, method_name, event_dict):  # pylint: disable=unused-argument
    return collections.OrderedDict(
        sorted(event_dict.items(), key=lambda item: (item[0] != "event", item))
    )


def _setup_once():

    structlog.configure_once(
        processors=[
            structlog.stdlib.add_logger_name,  # optional, but before SentryProcessor()
            structlog.stdlib.add_log_level,  # required before SentryProcessor()
            SentryProcessor(level=logging.ERROR),
            structlog.stdlib.filter_by_level,
            _add_caller_info,
            _add_log_level,
            _add_thread_info,
            _event_uppercase,
            # structlog.stdlib.add_logger_name,  # Typically a duplicate of "_module"
            structlog.stdlib.PositionalArgumentsFormatter(True),
            _add_timestamp,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeEncoder()
            if sys.version_info.major == 2
            else structlog.processors.UnicodeDecoder(),
            _order_keys,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logger = get_logger(__name__)

    if config[env].USE_LOG_FILE:
        logging.config.dictConfig(LOGGING_CONFIG)
        logger.info(
            "logging_initialized",
            logger_level=LOGGING_CONFIG["loggers"][BASE_LOGGER_NAME]["level"].lower(),
            logfile=LOGGING_CONFIG["handlers"]["file"]["filename"],
        )
    else:
        logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)


def get_logger(logger_name=None):
    global IS_CONFIGURED  # pylint: disable=global-statement
    if not IS_CONFIGURED:
        IS_CONFIGURED = True
        _setup_once()
    if logger_name is None:
        logger_name = inspect.currentframe().f_back.f_globals["__name__"]
    logger_name = BASE_LOGGER_NAME if logger_name == "__main__" else logger_name
    return structlog.wrap_logger(logging.getLogger(logger_name))
