import sentry_sdk
from sentry_dramatiq import DramatiqIntegration
from sentry_sdk import configure_scope
from sentry_sdk.integrations.django import DjangoIntegration


def initialize_sentry(dsn: str, environment: str) -> None:
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration(), DramatiqIntegration()],
        environment=environment,
        debug=True,
        request_bodies="always",
        send_default_pii=True,
        traces_sample_rate=0.1,
    )


def sentry_dont_track_performance() -> None:
    with configure_scope() as sentry_scope:
        if sentry_scope.transaction:
            sentry_scope.transaction.sampled = False
