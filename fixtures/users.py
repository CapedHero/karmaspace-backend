import django


django.setup()

from fixtures.constants import USER_1_ID
from src.app_auth.models import User


admin = User(
    username="admin",
    email="admin@admin.admin",
    is_superuser=True,
    is_staff=True,
)
admin.set_password("admin")
admin.save()

User.objects.create(
    id=USER_1_ID,
    username="CapedHero",
    email="mc.wrzesniewski@gmail.com",
)
