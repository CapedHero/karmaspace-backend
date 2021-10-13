import django  # isort:skip


django.setup()

from src.app_auth.models import User
from src.core.mailchimp import subscribe_email


if __name__ == "__main__":
    for user in User.objects.filter(is_demo=False):
        subscribe_email(user.email)
