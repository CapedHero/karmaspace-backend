from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import bleach

from src.core.dramatiq_actors import dramatiq_actor


@dramatiq_actor()
def send_thank_you_for_joining_msg(user_email: str) -> None:
    msg_html = render_to_string(template_name="emails/thank_you_for_joining.html")
    send_mail(
        subject="Witaj w KarmaSpace!",
        html_message=msg_html,
        message=strip_tags(msg_html),
        from_email='"KarmaSpace" <welcome@karmaspace.io>',
        recipient_list=[user_email],
    )


@dramatiq_actor()
def send_new_user_created_msg_to_karmaspace_team(user_username: str, user_email: str) -> None:
    send_mail(
        subject=f"Nowy użytkownik - {user_username} | {user_email}",
        message="Nice!",
        from_email='"KarmaSpace News" <karmabot@karmaspace.io>',
        recipient_list=["news@karmaspace.io"],
    )


@dramatiq_actor()
def send_user_feedback(
    username: str,
    user_email: str,
    dangerous_user_msg: str,
) -> None:
    safe_user_msg = bleach.clean(dangerous_user_msg, tags=settings.EMAIL_ALLOWED_HTML_TAGS)
    ready_to_send_user_msg = bleach.linkify(safe_user_msg)

    send_mail(
        subject=f"Feedback - Nowa wiadomość od użytkownika {username} | {user_email}",
        html_message=ready_to_send_user_msg,
        message=strip_tags(ready_to_send_user_msg),
        from_email='"KarmaSpace Feedback" <karmabot@karmaspace.io>',
        recipient_list=["feedback@karmaspace.io"],
    )
