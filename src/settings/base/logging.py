"""
Code sourced from loguru docs:
+ https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
+ https://github.com/Delgan/loguru/issues/474#issuecomment-926705136
"""
import logging
import logging.config
import sys

from loguru import logger

from django_environ import env


class PropagateHandler(logging.Handler):
    def emit(self, record):
        record.from_loguru = True
        logging.getLogger(record.name).handle(record)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Ignore messages from PropagateHandler to avoid hanging
        if getattr(record, "from_loguru", False):
            return

        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


LOGGERS = list(logging.root.manager.loggerDict) + ["werkzeug"]
STANDARD_CONFIG = {
    "handlers": ["intercept"],
    "level": env("APP_LOG_LEVEL", default="DEBUG"),
    "propagate": True,
}
loggers_configs = {logger: STANDARD_CONFIG.copy() for logger in LOGGERS}

# Handle spammers.
SPAMMERS = ["asyncio", "dramatiq", "django", "faker.factory", "sentry", "sentry_sdk"]
for spammer in SPAMMERS:
    try:
        loggers_configs[spammer]["level"] = "INFO"
    except KeyError:
        pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "intercept": {
            "()": InterceptHandler,
            "level": 0,
        },
    },
    "loggers": loggers_configs,
}

logger.remove()
# SPECIFIC logger.add(...) are handled in settings local.py/prod.py/test.py!
