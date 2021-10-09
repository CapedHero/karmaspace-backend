from typing import List

from django.conf import settings
from django.core.mail import send_mail as dj_send_email
from django.utils.html import strip_tags


def send_email(
    *,
    subject: str,
    body_html: str = "",
    body_txt: str = "",
    from_email: str,
    to_emails: List[str],
) -> None:
    filtered_to_emails = [
        email for email in to_emails if not email.endswith(settings.DEMO_USER_EMAIL_DOMAIN)
    ]
    if body_txt:
        body_text_ = body_txt
    else:
        body_text_ = strip_tags(body_html)
        if not body_text_:
            return

    dj_send_email(
        subject=subject,
        html_message=body_html,
        message=body_text_,
        from_email=from_email,
        recipient_list=filtered_to_emails,
    )
