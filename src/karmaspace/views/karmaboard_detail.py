from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from src.core.permissions import IsOwner
from ..models import KarmaBoard
from ..serializers import KarmaSpaceSerializer


class GetOutputSerializer(KarmaSpaceSerializer):
    ...


class PatchInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaBoard
        fields = ["name"]


class PatchOutputSerializer(KarmaSpaceSerializer):
    ...


class KarmaBoardDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request: Request, owner_username: str, slug: str) -> Response:
        db_obj = get_object_or_404(KarmaBoard, owner__username=owner_username, slug=slug)
        output = GetOutputSerializer(db_obj).data
        return Response(data=output, status=HTTP_200_OK)

    def patch(self, request: Request, owner_username: str, slug: str) -> Response:
        db_obj = get_object_or_404(KarmaBoard, owner__username=owner_username, slug=slug)
        input_ = PatchInputSerializer(db_obj, data=request.data, partial=True)
        input_.is_valid(raise_exception=True)
        instance = input_.save()
        output = GetOutputSerializer(instance).data
        return Response(data=output, status=HTTP_200_OK)