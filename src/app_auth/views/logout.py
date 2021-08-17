from django.contrib.auth import logout
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


@api_view(http_method_names=["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def logout_view(request: Request) -> Response:
    logout(request)
    return Response(data={}, status=HTTP_200_OK)
