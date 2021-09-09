from rest_framework import serializers

from src.app_auth.models import User
from .models import Karma, KarmaBoard
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
        fields = ["id", "name", "value", "duration_in_m", "created_at"]


class KarmaBoardSerializer(serializers.ModelSerializer):
    class OwnerSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username"]

    class Meta:
        model = KarmaBoard
        fields = ["id", "owner", "name", "value_step", "unsplash_photo", "sort_index"]

    owner = OwnerSerializer()
    unsplash_photo = UnsplashPhotoSerializer()
