from django_environ import env
from src.core.sentry import initialize_sentry


SENTRY_IS_ENABLED = env.bool("SENTRY_IS_ENABLED", default=False)
if SENTRY_IS_ENABLED:
    SENTRY_BE_DSN = env("SENTRY_BE_DSN")
    SENTRY_FE_DSN = env("SENTRY_FE_DSN")
    SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT")
    initialize_sentry(SENTRY_BE_DSN, SENTRY_ENVIRONMENT)
