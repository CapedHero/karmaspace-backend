from rest_framework import serializers

from src.app_auth.models import User
from .models import Karma, KarmaBoard, KarmaBoardUser
from .models.unsplash_photo import UnsplashPhoto


class UnsplashPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnsplashPhoto
        fields = ["id", "regular_url", "small_url", "author_name", "author_url"]

    # We need to configure id field manually, as we don't want unique ID
    # ValidationError to be raised.
    id = serializers.CharField(max_length=50)


class KarmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karma
        fields = [
            "id",
            "name",
            "value",
            "duration_in_m",
            "is_task",
            "created_at",
            "completed_at",
            "note",
        ]


class KarmaBoardSerializer(serializers.ModelSerializer):
    class OwnerSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username"]

    class Meta:
        model = KarmaBoard
        fields = ["id", "owner", "name", "value_step", "unsplash_photo", "sort_index"]

    owner = OwnerSerializer()
    sort_index = serializers.SerializerMethodField(method_name="get_sort_index")
    unsplash_photo = UnsplashPhotoSerializer()

    def get_sort_index(self, karmaboard: KarmaBoard) -> float:
        return KarmaBoardUser.objects.get(
            karmaboard=karmaboard,
            user=self.context["user"],
        ).sort_index


class KarmaBoardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaBoardUser
        fields = ["id", "username", "role"]

    id = serializers.CharField(source="user.id")
    username = serializers.CharField(source="user.username")
    role = serializers.CharField(source="user_role")
