from uuid import UUID

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from src.core.permissions import IsOwnerOrMember
from ..models import Karma


class PatchInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karma
        fields = ["name", "value", "duration_in_m", "is_task", "completed_at", "note"]


class KarmaDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def patch(self, request: Request, pk: UUID) -> Response:
        db_obj = get_object_or_404(Karma, pk=pk)
        self.check_object_permissions(self.request, db_obj.karmaboard)
        input_ = PatchInputSerializer(db_obj, data=request.data, partial=True)
        input_.is_valid(raise_exception=True)
        input_.save()
        return Response(data={}, status=HTTP_200_OK)

    def delete(self, request: Request, pk: UUID) -> Response:
        db_obj = get_object_or_404(Karma, pk=pk)
        self.check_object_permissions(self.request, db_obj.karmaboard)
        db_obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
