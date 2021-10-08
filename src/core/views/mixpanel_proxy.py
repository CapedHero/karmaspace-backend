from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import FormParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

import backoff
import requests

from src.core import time_units
from src.core.networking import session


@api_view(http_method_names=["GET", "POST"])
@csrf_exempt
@authentication_classes([])
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

    mixpanel_response = _robust_session_request(
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


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=requests.ConnectionError,
    max_time=time_units.in_s.SEC_15,
)
def _robust_session_request(*args, **kwargs) -> requests.Response:
    return session.request(*args, **kwargs)
