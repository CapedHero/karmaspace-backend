from rest_framework import serializers

from src.app_auth.models import User
from .models import Karma, KarmaBoard


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
        fields = ["id", "owner", "name", "value_step", "sort_index"]

    owner = OwnerSerializer()
