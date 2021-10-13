from django.conf import settings

from loguru import logger
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


mailchimp = Client()
mailchimp.set_config(
    {
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": settings.MAILCHIMP_DATA_CENTER,
    }
)


def subscribe_email(email: str) -> None:
    try:
        mailchimp.lists.add_list_member(
            list_id=settings.MAILCHIMP_EMAIL_LIST_ID,
            body={"email_address": email, "status": "subscribed"},
        )
    except ApiClientError:
        logger.exception("Mailchimp API error.")
