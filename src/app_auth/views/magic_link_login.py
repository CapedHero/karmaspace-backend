from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from src.core.utils import add_safely_query_params


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def magic_link_login_view(request: Request) -> HttpResponseRedirect:
    redirect_url = request.query_params["redirect_url"]
    redirect_url = add_safely_query_params(redirect_url, params={"login_method": "magic_link"})
    return redirect(redirect_url, permanent=False)
