from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.networking import session


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def unsplash_proxy_view(request: Request, api_path: str) -> Response:
    relayed_querystring = request.query_params.urlencode()
    url = f"https://api.unsplash.com/{api_path}?{relayed_querystring}"
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}

    unsplash_response = session.get(url, headers=headers)

    dj_response = Response(data=unsplash_response.json(), status=unsplash_response.status_code)
    if "X-Total" in unsplash_response.headers:
        dj_response.headers["X-Total"] = unsplash_response.headers["X-Total"]

    return dj_response
