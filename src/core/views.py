import json

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

import requests

from .sentry import sentry_dont_track_performance


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def health_view(request: Request) -> Response:
    sentry_dont_track_performance()
    # https://tools.ietf.org/id/draft-inadarei-api-health-check-01.html
    return Response(data={"status": "pass"})


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def sentry_tunnel_view(request: Request) -> Response:
    if not settings.SENTRY_IS_ENABLED:
        return Response(
            data={"detail": "Sentry is not enabled."},
            status=HTTP_400_BAD_REQUEST,
        )

    headers = json.loads(request.body.splitlines()[0])
    try:
        dsn = headers["dsn"]
    except KeyError:
        return Response(
            data={"detail": f"Missing Sentry DSN header. headers={headers}"},
            status=HTTP_400_BAD_REQUEST,
        )

    if dsn != settings.SENTRY_FE_DSN:
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


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def unsplash_proxy_view(request: Request, api_path: str) -> Response:
    relayed_querystring = request.query_params.urlencode()
    url = f"https://api.unsplash.com/{api_path}?{relayed_querystring}"
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
    unsplash_response = requests.get(url, headers=headers)
    return Response(data=unsplash_response.json(), status=unsplash_response.status_code)
