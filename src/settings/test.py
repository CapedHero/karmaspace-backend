import tempfile

from loguru import logger

from .base import *


ADMIN_BASE_PATH = "test-admin/"
DEBUG = True
DEFAULT_FROM_EMAIL = "test-bot@karmaspace.com"
MEDIA_ROOT = tempfile.gettempdir()
MEDIA_URL = "https://test.com/media/"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.stub.StubBroker",
    "OPTIONS": {},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ],
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

logger.add(sys.stderr)
# Pytest needs to capture the logs and to do so, logs need to be propagated
# to its LogCaptureHandler.
logger.add(PropagateHandler(), format="{message}")
