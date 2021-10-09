from django.db import IntegrityError, transaction
from django.template.loader import render_to_string

from dateutil.relativedelta import relativedelta

from src.app_auth.models import User
from src.core.dramatiq_actors import dramatiq_actor
from src.core.email import send_email
from src.core.utils import get_today_hh_mm
from ..models import Job


JOB_NAME = "send_follow_up_email_after_joining"


@dramatiq_actor()
def send_follow_up_email_after_joining() -> None:
    today_midnight = get_today_hh_mm("00:00")
    yesterday_midnight = today_midnight - relativedelta(days=1)

    users_created_yesterday = User.objects.filter(
        created_at__gte=yesterday_midnight,
        created_at__lte=today_midnight,
    )

    for user in users_created_yesterday:
        if _is_job_already_handled(user):
            continue

        try:
            with transaction.atomic():
                job = Job(name=JOB_NAME, marker=str(user.id))

                job.status = Job.Status.IN_PROGRESS
                job.save()

                msg_html = render_to_string(template_name="emails/follow_up_after_joining.html")
                send_email(
                    subject="To wspaniale, że z nami jesteś 💜",
                    body_html=msg_html,
                    from_email='"KarmaSpace" <hello@karmaspace.io>',
                    to_emails=[user.email],
                )

                job.status = Job.Status.DONE
                job.save()

        except IntegrityError:
            return


def _is_job_already_handled(user: User) -> bool:
    return Job.objects.filter(name=JOB_NAME, marker=str(user.id)).exists()
