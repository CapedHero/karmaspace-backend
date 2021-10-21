from datetime import date

from django.db import IntegrityError, transaction
from django.template.loader import render_to_string

from dateutil.relativedelta import relativedelta

from src.core.dramatiq_actors import dramatiq_actor
from src.core.email import send_email
from src.core.utils import get_today_hh_mm
from src.karmaspace.models import Karma, KarmaBoard
from ..models import Job


JOB_NAME = "send_report_yesterday_created_karmaboards_and_karmas"


@dramatiq_actor()
def send_report_yesterday_created_karmaboards_and_karmas() -> None:
    if _is_job_already_done():
        return

    today_midnight = get_today_hh_mm("00:00")
    yesterday_midnight = today_midnight - relativedelta(days=1)

    non_demo_karmaboards_created_yesterday = KarmaBoard.objects.filter(
        created_at__gte=yesterday_midnight,
        created_at__lt=today_midnight,
    ).exclude(owner__is_demo=True)

    non_demo_karmas_created_yesterday = Karma.objects.filter(
        created_at__gte=yesterday_midnight,
        created_at__lt=today_midnight,
    ).exclude(karmaboard__owner__is_demo=True)

    try:
        with transaction.atomic():
            job = Job(name=JOB_NAME, marker=_get_marker())

            job.status = Job.Status.IN_PROGRESS
            job.save()

            msg_html = render_to_string(
                template_name="emails/report_karmaboards_and_karmas.html",
                context={
                    "karmaboards": non_demo_karmaboards_created_yesterday,
                    "karmas": non_demo_karmas_created_yesterday,
                },
            )
            send_email(
                subject="Karmaboardy i Karmy utworzone wczoraj",
                body_html=msg_html,
                from_email='"KarmaSpace Reports" <karmabot@karmaspace.io>',
                to_emails=["maciej.wrzesniewski@karmaspace.io"],
            )

            job.status = Job.Status.DONE
            job.save()

    except IntegrityError:
        return


def _is_job_already_done() -> bool:
    return Job.objects.filter(name=JOB_NAME, marker=_get_marker()).exists()


def _get_marker() -> str:
    return str(date.today())
