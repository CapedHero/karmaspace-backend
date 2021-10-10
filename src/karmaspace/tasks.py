from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    dangerous_user_msg: str,
    user_pk: str = "",
) -> None:
    is_empty_msg = len(strip_tags(dangerous_user_msg)) == 0
    if is_empty_msg:
        return

    safe_user_msg = bleach.clean(dangerous_user_msg, tags=settings.EMAIL_ALLOWED_HTML_TAGS)
    ready_to_send_user_msg = bleach.linkify(safe_user_msg)

    if user_pk:
        from src.app_auth.models import User  # Prevent circular imports

        user = User.objects.get(pk=user_pk)
        subject = f"Nowa wiadomość od użytkownika {user.username}"
        ready_to_send_user_msg += (
            f'<hr><div>Email użytkownika: <a href="mailto:{user.email}">{user.email}</a></div>'
        )
    else:
        subject = "Nowa anonimowa wiadomość"

    send_email(
        subject=subject,
        body_html=ready_to_send_user_msg,
        from_email='"KarmaSpace Feedback" <karmabot@karmaspace.io>',
        to_emails=["feedback@karmaspace.io"],
    )
