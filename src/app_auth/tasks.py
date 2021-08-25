from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from src.core.dramatiq_actors import dramatiq_actor


@dramatiq_actor()
def send_passphrase_to_user(user_email: str, passphrase: str) -> None:
    msg_html = render_to_string(
        template_name="emails/passphrase.html",
        context={"passphrase": passphrase},
    )
    send_mail(
        subject=f"Twoje tymczasowe hasło do KarmaSpace to {passphrase}",
        html_message=msg_html,
        message=strip_tags(msg_html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
