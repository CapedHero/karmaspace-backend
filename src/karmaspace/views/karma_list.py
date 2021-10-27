from typing import Any
from uuid import UUID

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from src.core.permissions import IsOwnerOrMember
from ..models import Karma, KarmaBoard
from ..serializers import KarmaSerializer


class PostInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karma
        fields = ["name", "value", "duration_in_m", "is_active_task", "completed_at", "note"]

    def create(self, validated_data: Any) -> Karma:
        return Karma.objects.create(karmaboard=self.context["karmaboard"], **validated_data)


class PostOutputSerializer(KarmaSerializer):
    ...


class KarmaListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def post(self, request: Request, karmaboard_pk: UUID) -> Response:
        karmaboard = get_object_or_404(KarmaBoard, pk=karmaboard_pk)
        self.check_object_permissions(self.request, karmaboard)
        input_ = PostInputSerializer(data=request.data, context={"karmaboard": karmaboard})
        input_.is_valid(raise_exception=True)
        instance = input_.save()
        output = PostOutputSerializer(instance).data
        return Response(data=output, status=HTTP_201_CREATED)
