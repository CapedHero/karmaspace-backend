from django.conf import settings
from django.template.loader import render_to_string

from sesame.utils import get_query_string

from src.app_auth.models import User
from src.core.dramatiq_actors import dramatiq_actor
from src.core.email import send_email


@dramatiq_actor()
def send_passphrase_to_user(user_email: str, passphrase: str, redirect_url: str) -> None:
    try:
        user = User.objects.get(email=user_email)
        magic_link = (
            settings.FRONTEND_BASE_URL
            + "/auth/magic-link"
            + get_query_string(user)
            + f"&redirectURL={redirect_url}"
        )
    except User.DoesNotExist:
        magic_link = None
    msg_html = render_to_string(
        template_name="emails/passphrase.html",
        context={"passphrase": passphrase, "magic_link": magic_link},
    )
    send_email(
        subject="Logowanie do KarmaSpace",
        body_html=msg_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=[user_email],
    )
