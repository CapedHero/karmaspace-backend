from typing import Any

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from src.app_auth.models import User
from src.core.permissions import IsOwner
from ..models import KarmaBoard


class GetOutputSerializer(serializers.ModelSerializer):
    class OwnerSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username"]

    class Meta:
        model = KarmaBoard
        fields = ["owner", "name", "slug"]

    owner = OwnerSerializer()


class PostInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaBoard
        fields = ["name"]

    def create(self, validated_data: Any) -> KarmaBoard:
        return KarmaBoard.objects.create(owner=self.context["owner"], **validated_data)


class KarmaBoardListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request: Request) -> Response:
        karmaboards = KarmaBoard.objects.filter(owner=request.user).order_by("name")
        output = GetOutputSerializer(karmaboards, many=True).data
        return Response(data=output, status=HTTP_200_OK)

    def post(self, request: Request) -> Response:
        input_ = PostInputSerializer(data=request.data, context={"owner": request.user})
        input_.is_valid(raise_exception=True)
        input_.save()
        return Response(data={}, status=HTTP_201_CREATED)
