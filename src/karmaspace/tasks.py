from django.conf import settings
from django.template.loader import render_to_string

import bleach

from src.core.dramatiq_actors import dramatiq_actor
from src.core.email import send_email


@dramatiq_actor()
def send_thank_you_for_joining_msg(user_email: str) -> None:
    msg_html = render_to_string(template_name="emails/thank_you_for_joining.html")
    send_email(
        subject="Witaj w KarmaSpace!",
        body_html=msg_html,
        from_email='"KarmaSpace" <hello@karmaspace.io>',
        to_emails=[user_email],
    )


@dramatiq_actor()
def send_new_user_created_msg_to_karmaspace_team(user_username: str, user_email: str) -> None:
    send_email(
        subject=f"Nowy użytkownik - {user_username} | {user_email}",
        body_txt="Nice!",
        from_email='"KarmaSpace News" <karmabot@karmaspace.io>',
        to_emails=["news@karmaspace.io"],
    )


@dramatiq_actor()
def send_user_feedback(
    username: str,
    user_email: str,
    dangerous_user_msg: str,
) -> None:
    safe_user_msg = bleach.clean(dangerous_user_msg, tags=settings.EMAIL_ALLOWED_HTML_TAGS)
    ready_to_send_user_msg = bleach.linkify(safe_user_msg)

    send_email(
        subject=f"Feedback - Nowa wiadomość od użytkownika {username} | {user_email}",
        body_html=ready_to_send_user_msg,
        from_email='"KarmaSpace Feedback" <karmabot@karmaspace.io>',
        to_emails=["feedback@karmaspace.io"],
    )
