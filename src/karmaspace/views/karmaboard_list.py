from typing import Any, Dict

from django.db import transaction
from django.db.models.aggregates import Sum
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from ..models import KarmaBoard, UnsplashPhoto
from ..models.crud.creators import create_karmaboard
from ..serializers import KarmaBoardSerializer, KarmaBoardUserSerializer, UnsplashPhotoSerializer


class PostInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaBoard
        fields = ["name", "value_step", "unsplash_photo", "invitation_secret"]

    invitation_secret = serializers.CharField()
    unsplash_photo = UnsplashPhotoSerializer()

    @transaction.atomic
    def create(self, validated_data: Any) -> KarmaBoard:
        invitation_secret = validated_data.pop("invitation_secret")
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
        return create_karmaboard(
            owner=self.context["owner"],
            unsplash_photo=unsplash_photo,
            invitation_secret=invitation_secret,
            **validated_data,
        )


class PostOutputSerializer(KarmaBoardSerializer):
    ...


class GetOutputSerializer(KarmaBoardSerializer):
    class Meta(KarmaBoardSerializer.Meta):
        fields = [*KarmaBoardSerializer.Meta.fields, "total_karmas_value", "users"]

    total_karmas_value = serializers.IntegerField()
    users = serializers.SerializerMethodField(method_name="get_users")

    def get_users(self, karmaboard: KarmaBoard) -> Dict[str, str]:
        return KarmaBoardUserSerializer(karmaboard.karmaboarduser_set.all(), many=True).data


class KarmaBoardListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        input_ = PostInputSerializer(data=request.data, context={"owner": request.user})
        input_.is_valid(raise_exception=True)
        instance = input_.save()
        output = PostOutputSerializer(instance, context={"user": request.user}).data
        return Response(data=output, status=HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        karmaboards = (
            KarmaBoard.objects.filter(karmaboarduser__user=request.user)
            .prefetch_related("karmaboarduser_set")
            .annotate(total_karmas_value=Sum("karmas__value"))
            .order_by("karmaboarduser__sort_index")
        )
        output = GetOutputSerializer(karmaboards, many=True, context={"user": request.user}).data
        return Response(data=output, status=HTTP_200_OK)
