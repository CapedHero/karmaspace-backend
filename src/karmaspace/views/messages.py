from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from ..tasks import send_user_feedback


class PostInputSerializer(serializers.Serializer):
    msg = serializers.CharField()


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def user_feedback_view(request: Request) -> Response:
    serializer = PostInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dangerous_user_msg = serializer.validated_data["msg"]

    if isinstance(request.user, AnonymousUser):
        send_user_feedback.send(dangerous_user_msg)
    else:
        send_user_feedback.send(dangerous_user_msg, str(request.user.pk))

    return Response(data={}, status=HTTP_201_CREATED)
