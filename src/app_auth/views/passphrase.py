from datetime import datetime, timezone

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from dateutil.relativedelta import relativedelta

from ..models import PassphraseRecord
from ..passphrase import get_passphrase
from ..tasks import send_passphrase_to_user


class PostInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    redirect_url = serializers.URLField(default="", allow_blank=True)


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def passphrase_view(request: Request) -> Response:
    serializer = PostInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_email = serializer.validated_data["email"]
    passphrase = get_passphrase()
    expires_at = datetime.now(timezone.utc) + relativedelta(minutes=15)

    PassphraseRecord.objects.filter(email=user_email).delete()
    PassphraseRecord.objects.create(email=user_email, passphrase=passphrase, expires_at=expires_at)

    send_passphrase_to_user.send(
        user_email,
        passphrase,
        serializer.validated_data["redirect_url"],
    )
    return Response(data={}, status=HTTP_201_CREATED)
