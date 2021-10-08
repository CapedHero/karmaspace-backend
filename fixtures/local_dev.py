import django  # isort:skip


django.setup()


from django.conf import settings

from fixtures import models
from fixtures.demo import create_demo_for_user
from src.app_auth.models import User


models.create_admin()

demo_user = User.objects.create(
    username=settings.FIXTURES_USER_1_USERNAME,
    email=settings.FIXTURES_USER_1_EMAIL,
)
create_demo_for_user(demo_user)
