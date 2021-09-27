import sys

from django_environ import env


LOGGERS = [
    "django",
    "dramatiq",
    "gunicorn.access",
    "gunicorn.error",
    "main",
    "sentry",
    "sentry_sdk",
    "sentry_sdk.errors",
    "werkzeug",
]
STANDARD_CONFIG = {
    "handlers": ["stderr"],
    "level": env("APP_LOG_LEVEL", default="DEBUG"),
    "propagate": True,
}
loggers_configs = {logger: STANDARD_CONFIG.copy() for logger in LOGGERS}

# Handle spammers.
loggers_configs["django"]["level"] = "INFO"
loggers_configs["sentry_sdk"]["level"] = "INFO"
loggers_configs["sentry_sdk.errors"]["level"] = "INFO"

DICT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "%(asctime)s %(name)s %(levelname)s %(message)s"}},
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": sys.stderr,
        }
    },
    "loggers": loggers_configs,
}
