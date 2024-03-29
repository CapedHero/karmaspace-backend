from django.conf import settings
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from fixtures.demo import create_demo_for_user
from src.app_auth.models import User
from src.core.utils import create_random_string


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def demo_view(request: Request) -> Response:
    random_string = create_random_string(chars_num=8)

    demo_user = User.objects.create(
        username=f"DemoUser-{random_string}",
        email=f"demo-user-{random_string}@{settings.DEMO_USER_EMAIL_DOMAIN}",
        is_demo=True,
    )

    login(request, demo_user, backend="django.contrib.auth.backends.ModelBackend")

    create_demo_for_user(demo_user)

    return Response(status=HTTP_200_OK)
