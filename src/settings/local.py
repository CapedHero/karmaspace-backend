from loguru import logger

from django_environ import env
from .base import *


DEBUG = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

ADMIN_BASE_PATH = "admin/"

INSTALLED_APPS += [
    "django_extensions",
    # "silk",
]

MIDDLEWARE += [
    "src.core.middlewares.BetterExceptionsMiddleware",
    # "silk.middleware.SilkyMiddleware",
]

FIXTURES_USER_1_USERNAME = env("FIXTURES_USER_1_USERNAME")
FIXTURES_USER_1_EMAIL = env("FIXTURES_USER_1_EMAIL")

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = PROJECT_ROOT / "profiles"
SILKY_META = True

SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = ["localhost:8080"]

logger.add(sys.stderr)
