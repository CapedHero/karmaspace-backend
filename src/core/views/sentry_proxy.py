import json
import logging

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

import requests


logger = logging.getLogger("main")


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def sentry_proxy_view(request: Request) -> Response:  # noqa: C901
    if not settings.SENTRY_IS_ENABLED:
        return Response(
            data={"detail": "Sentry is not enabled."},
            status=HTTP_400_BAD_REQUEST,
        )

    envelope = request.body.splitlines()
    try:
        envelope_headers, item_headers, item = map(lambda x: json.loads(x), envelope)
    except ValueError:
        logger.exception(
            msg="Sentry Proxy Error. Unexpected request body.",
            extra={"request_body": request.body},
        )
        return Response(
            data={"detail": "Unexpected request body."},
            status=HTTP_400_BAD_REQUEST,
        )

    try:
        dsn = envelope_headers["dsn"]
    except KeyError:
        if item_headers.get("type", "") == "client_report":
            logger.error(
                msg="Sentry Proxy Error. Event not sent.",
                extra={"request_body": request.body},
            )
            return Response(
                data={"detail": "Event not sent due to a client error."},
                status=HTTP_400_BAD_REQUEST,
            )

        logger.exception(
            msg="Sentry Proxy Error. Missing Sentry DSN header.",
            extra={"request_body": request.body},
        )
        return Response(
            data={"detail": "Missing Sentry DSN header."},
            status=HTTP_400_BAD_REQUEST,
        )

    if dsn != settings.SENTRY_FE_DSN:
        logger.exception(
            msg="Sentry Proxy Error. Sentry DSN doesn't match.",
            extra={"request_body": request.body},
        )
        return Response(
            data={"detail": "Sentry DSN doesn't match."},
            status=HTTP_400_BAD_REQUEST,
        )

    sentry_project_id = dsn.rsplit("/", maxsplit=1)[1]
    url = f"https://sentry.io/api/{sentry_project_id}/envelope/"
    sentry_response = requests.post(
        url=url,
        data=request.body,
        headers={"Content-Type": "application/x-sentry-envelope"},
    )
    if sentry_response.status_code >= 400:
        return Response(
            data={
                "detail": (
                    f"Sentry responded with error. "
                    f"url={url}, "
                    f"status_code={sentry_response.status_code}, "
                    f"body={sentry_response.json()}"
                )
            },
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(status=sentry_response.status_code)
