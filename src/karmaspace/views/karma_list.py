from typing import Any

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from src.core.permissions import IsOwner
from ..models import Karma, KarmaBoard


class PostInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karma
        fields = ["name", "value"]

    def create(self, validated_data: Any) -> Karma:
        karmaboard = KarmaBoard.objects.get(
            owner__username=self.context["karmaboard_owner_username"],
            slug=self.context["karmaboard_slug"],
        )
        return Karma.objects.create(karmaboard=karmaboard, **validated_data)


class PostOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karma
        fields = ["id", "created_at", "name", "value"]


class KarmaListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(
        self,
        request: Request,
        karmaboard_owner_username: str,
        karmaboard_slug: str,
    ) -> Response:
        input_ = PostInputSerializer(
            data=request.data,
            context={
                "karmaboard_owner_username": karmaboard_owner_username,
                "karmaboard_slug": karmaboard_slug
            })
        input_.is_valid(raise_exception=True)
        instance = input_.save()
        output = PostOutputSerializer(instance).data
        return Response(data=output, status=HTTP_201_CREATED)
