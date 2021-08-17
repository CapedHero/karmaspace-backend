from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .sentry import sentry_dont_track_performance


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def health_view(request: Request) -> Response:
    sentry_dont_track_performance()
    # https://tools.ietf.org/id/draft-inadarei-api-health-check-01.html
    return Response(data={"status": "pass"})
