from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from ..models import User


class GetOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def user_me_view(request: Request) -> Response:
    output = GetOutputSerializer(request.user).data
    return Response(data=output, status=HTTP_200_OK)
