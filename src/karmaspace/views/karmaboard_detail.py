from typing import Any, Dict
from uuid import UUID

from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from src.core.permissions import IsOwnerOrMember
from ..models import KarmaBoard, KarmaBoardInvitation, KarmaBoardUser
from ..models.unsplash_photo import UnsplashPhoto
from ..serializers import KarmaBoardSerializer, KarmaSerializer, UnsplashPhotoSerializer


class GetOutputSerializer(KarmaBoardSerializer):
    class Meta(KarmaBoardSerializer.Meta):
        fields = [*KarmaBoardSerializer.Meta.fields, "karmas", "invitation_secret"]

    karmas = serializers.SerializerMethodField(method_name="get_karmas")
    invitation_secret = serializers.SerializerMethodField(method_name="get_invitation_secret")

    def get_karmas(self, karmaboard: KarmaBoard) -> Dict[str, Dict[str, Any]]:
        karmas = karmaboard.karmas.all().order_by("-created_at")
        return KarmaSerializer(karmas, many=True).data

    def get_invitation_secret(self, karmaboard: KarmaBoard) -> str:
        return KarmaBoardInvitation.objects.get(karmaboard=karmaboard).secret


class PatchInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaBoard
        fields = ["name", "value_step", "unsplash_photo", "sort_index"]

    sort_index = serializers.FloatField()
    unsplash_photo = UnsplashPhotoSerializer()

    @transaction.atomic
    def update(self, instance: KarmaBoard, validated_data: Any) -> KarmaBoard:
        photo_data = validated_data.pop("unsplash_photo", None)
        sort_index = validated_data.pop("sort_index", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if photo_data:
            unsplash_photo, _ = UnsplashPhoto.objects.update_or_create(
                id=photo_data["id"],
                defaults={
                    "regular_url": photo_data["regular_url"],
                    "small_url": photo_data["small_url"],
                    "author_name": photo_data["author_name"],
                    "author_url": photo_data["author_url"],
                },
            )
            instance.unsplash_photo = unsplash_photo

        if sort_index:
            karmaboard_user = KarmaBoardUser.objects.get(
                karmaboard=instance,
                user=self.context["user"],
            )
            karmaboard_user.sort_index = sort_index
            karmaboard_user.save()

        instance.save()

        return instance


class PatchOutputSerializer(KarmaBoardSerializer):
    ...


class KarmaBoardDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get(self, request: Request, pk: UUID) -> Response:
        db_obj = get_object_or_404(KarmaBoard, pk=pk)
        self.check_object_permissions(self.request, db_obj)
        output = GetOutputSerializer(db_obj, context={"user": request.user}).data
        return Response(data=output, status=HTTP_200_OK)

    def patch(self, request: Request, pk: UUID) -> Response:
        db_obj = get_object_or_404(KarmaBoard, pk=pk)
        self.check_object_permissions(self.request, db_obj)
        input_ = PatchInputSerializer(
            db_obj,
            data=request.data,
            partial=True,
            context={"user": request.user},
        )
        input_.is_valid(raise_exception=True)
        instance = input_.save()
        output = PatchOutputSerializer(instance, context={"user": request.user}).data
        return Response(data=output, status=HTTP_200_OK)

    def delete(self, request: Request, pk: UUID) -> Response:
        db_obj = get_object_or_404(KarmaBoard, pk=pk)
        self.check_object_permissions(self.request, db_obj)
        db_obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
