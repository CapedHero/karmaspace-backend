from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from src.core.permissions import IsOwner
from ..models import Karma


class PatchInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karma
        fields = ["name", "value"]


class KarmaDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request: Request, id_: str) -> Response:
        db_obj = get_object_or_404(Karma, id=id_)
        self.check_object_permissions(self.request, db_obj.karmaboard)
        input_ = PatchInputSerializer(db_obj, data=request.data, partial=True)
        input_.is_valid(raise_exception=True)
        input_.save()
        return Response(data={}, status=HTTP_200_OK)
