from typing import Any

from django.db import transaction
from django.db.models.aggregates import Sum
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from src.core.permissions import IsOwner
from ..models import KarmaBoard
from ..models.unsplash_photo import UnsplashPhoto
from ..serializers import KarmaBoardSerializer, UnsplashPhotoSerializer


class PostInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaBoard
        fields = ["name", "value_step", "unsplash_photo"]

    unsplash_photo = UnsplashPhotoSerializer()

    @transaction.atomic
    def create(self, validated_data: Any) -> KarmaBoard:
        photo_data = validated_data.pop("unsplash_photo")
        unsplash_photo, _ = UnsplashPhoto.objects.update_or_create(
            id=photo_data["id"],
            defaults={
                "regular_url": photo_data["regular_url"],
                "small_url": photo_data["small_url"],
                "author_name": photo_data["author_name"],
                "author_url": photo_data["author_url"],
            },
        )
        return KarmaBoard.objects.create(
            owner=self.context["owner"],
            unsplash_photo=unsplash_photo,
            **validated_data,
        )


class PostOutputSerializer(KarmaBoardSerializer):
    ...


class GetOutputSerializer(KarmaBoardSerializer):
    class Meta(KarmaBoardSerializer.Meta):
        fields = [*KarmaBoardSerializer.Meta.fields, "total_karmas_value"]

    total_karmas_value = serializers.IntegerField()


class KarmaBoardListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request: Request) -> Response:
        input_ = PostInputSerializer(data=request.data, context={"owner": request.user})
        input_.is_valid(raise_exception=True)
        instance = input_.save()
        output = PostOutputSerializer(instance).data
        return Response(data=output, status=HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        karmaboards = (
            KarmaBoard.objects.filter(owner=request.user)
            .annotate(total_karmas_value=Sum("karmas__value"))
            .order_by("name")
        )
        output = GetOutputSerializer(karmaboards, many=True).data
        return Response(data=output, status=HTTP_200_OK)
