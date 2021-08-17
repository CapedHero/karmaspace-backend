from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from src.core.permissions import IsAccessingOwnResourceOrReadOnly
from ..models import User


class GetOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar"]


class PatchInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar"]


class UserDetailView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsAccessingOwnResourceOrReadOnly]

    def get(self, request: Request, username: str) -> Response:
        db_obj = get_object_or_404(User, username=username)
        output = GetOutputSerializer(db_obj).data
        return Response(data=output, status=HTTP_200_OK)

    def patch(self, request: Request, username: str) -> Response:
        db_obj = get_object_or_404(User, username=username)
        input_ = PatchInputSerializer(db_obj, data=request.data, partial=True)
        input_.is_valid(raise_exception=True)
        input_.save()
        return Response(data={}, status=HTTP_200_OK)
