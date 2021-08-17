from django.contrib.auth import login
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from ..auth_logic import verify_email_ownership_with_passphrase
from ..models import User


class PostInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    passphrase = serializers.CharField(max_length=50)


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def passphrase_login_view(request: Request) -> Response:
    input_ = PostInputSerializer(data=request.data)
    input_.is_valid(raise_exception=True)

    email = input_.validated_data["email"]
    passphrase = input_.validated_data["passphrase"]

    is_verified_email_owner = verify_email_ownership_with_passphrase(email, passphrase)
    if not is_verified_email_owner:
        raise PermissionDenied()

    try:
        user = User.objects.get(email=email)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return Response(status=HTTP_200_OK)
    except User.DoesNotExist:
        raise PermissionDenied()
