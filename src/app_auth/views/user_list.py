from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView

from ..auth_logic import verify_email_ownership_with_passphrase
from ..models import User, UsernameValidator


class PostInputSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        max_length=50,
        validators=[UsernameValidator(), UniqueValidator(queryset=User.objects.all())],
    )
    passphrase = serializers.CharField(max_length=50)


class UserListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        input_ = PostInputSerializer(data=request.data)
        input_.is_valid(raise_exception=True)

        email = input_.validated_data["email"]
        username = input_.validated_data["username"]
        passphrase = input_.validated_data["passphrase"]

        is_verified_email_owner = verify_email_ownership_with_passphrase(email, passphrase)
        if not is_verified_email_owner:
            raise PermissionDenied()

        db_obj = User.objects.create(email=email, username=username)
        db_obj.save_random_avatar()

        return Response(data={}, status=HTTP_201_CREATED)

    def head(self, request: Request) -> Response:
        email = request.query_params.get("email")
        username = request.query_params.get("username")

        if (not email and not username) or (email and username):
            return Response(
                data={
                    "detail": 'Invalid query parameters. Please provide valid "email" OR "username".'
                },
                status=HTTP_400_BAD_REQUEST,
            )

        queryset = User.objects.all()
        if email:
            queryset = queryset.filter(email=email)
        elif username:
            queryset = queryset.filter(username=username)

        if queryset.exists():
            return Response(data={}, status=HTTP_200_OK)
        else:
            raise Http404()
