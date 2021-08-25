from rest_framework import serializers

from src.app_auth.models import User
from .models import KarmaBoard


class KarmaSpaceSerializer(serializers.ModelSerializer):
    class OwnerSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username"]

    class Meta:
        model = KarmaBoard
        fields = ["owner", "name", "slug"]

    owner = OwnerSerializer()
