from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

import requests


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
@parser_classes([FormParser])
def mixpanel_proxy_view(request: Request, api_path: str) -> Response:
    mixpanel_url = f"https://api-eu.mixpanel.com/{api_path}"
    ip = (
        request.META.get("HTTP_X_FORWARDED_FOR", {})
        or request.META.get("HTTP_X_REAL_IP", {})
        or request.META.get("REMOTE_ADDR", None)
    )
    headers = {"X-REAL-IP": ip}
    mixpanel_response = requests.request(
        method=request.method,
        url=mixpanel_url,
        headers=headers,
        params=request.query_params,
        data=request.data,
    )
    dj_response = Response(data=mixpanel_response.json(), status=mixpanel_response.status_code)
    for name, value in mixpanel_response.raw.headers.items():
        dj_response.headers[name] = value

    return dj_response
