from django.conf import settings
from django.core.mail import send_mail

from src.core.dramatiq_actors import dramatiq_actor


@dramatiq_actor()
def send_new_user_created_msg_to_karmaspace_team(user_username: str, user_email: str) -> None:
    send_mail(
        subject=f"Nowy użytkownik - {user_username} / {user_email}",
        message="Nice!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=settings.KARMASPACE_TEAM_EMAILS,
    )
