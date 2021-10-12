import django  # isort:skip


django.setup()


from django.conf import settings

from loguru import logger
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

from src.app_auth.models import User


def subscribe(email: str) -> None:
    mailchimp = Client()
    mailchimp.set_config(
        {
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_DATA_CENTER,
        }
    )

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        mailchimp.lists.add_list_member(settings.MAILCHIMP_EMAIL_LIST_ID, member_info)
    except ApiClientError:
        logger.exception("Mailchimp API error.")


if __name__ == "__main__":
    for user in User.objects.filter(is_demo=False):
        subscribe(user.email)
