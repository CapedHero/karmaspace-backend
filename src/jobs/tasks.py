import logging
from datetime import date, datetime, time

from django.db import IntegrityError, transaction
from django.db.models import IntegerField, OuterRef, Q, Subquery
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce

from pytz import timezone

from src.core.dramatiq_actors import dramatiq_actor
from src.karmaspace.models import Goal, KarmaBoard, Notification
from .models import Job


logger = logging.getLogger("main")
TZ = timezone("Europe/Warsaw")


@dramatiq_actor()
def run_periodic_jobs() -> None:
    logger.info("Periodic tasks triggered.")

    now = datetime.now(TZ)
    t_18_00 = _get_today_hh_mm("18:00")
    t_22_00 = _get_today_hh_mm("22:00")

    if t_18_00 <= now <= t_22_00:
        logger.info("create_daily_goals_notifications job scheduled.")
        create_daily_goals_notifications.send()


JOB_NAME = "create_daily_goals_notifications"


@dramatiq_actor()
def create_daily_goals_notifications() -> None:
    if Job.objects.filter(name=JOB_NAME, marker=str(date.today())).exists():
        return

    try:
        with transaction.atomic():
            job = Job.objects.create(
                name=JOB_NAME,
                marker=str(date.today()),
                status=Job.Status.IN_PROGRESS,
            )

            today_midnight = _get_today_hh_mm("00:00")

            today_karmas_per_karmaboard = KarmaBoard.objects.filter(
                id=OuterRef("karmaboard__id"),
            ).annotate(
                today_karmas_total_value=Sum(
                    "karmas__value",
                    filter=Q(karmas__created_at__gte=today_midnight),
                ),
            )
            daily_goals = Goal.objects.filter(timeframe=Goal.Timeframe.DAILY).annotate(
                today_total_karmas_value=Coalesce(
                    Subquery(
                        queryset=today_karmas_per_karmaboard.values("today_karmas_total_value"),
                        output_field=IntegerField(),
                    ),
                    0,
                ),
            )

            for goal in daily_goals:
                if goal.today_total_karmas_value < goal.target_value:
                    Notification.objects.create(
                        owner=goal.owner,
                        type=Notification.Type.GOAL,
                        content=(
                            f'KarmaBoard "{goal.karmaboard.name}": Brakuje Ci '
                            f"{goal.target_value - goal.today_total_karmas_value} "
                            f"Punktów Karmy do zrealizowania dziennego celu 🏁"
                        ),
                    )

            job.status = Job.Status.DONE
            job.save()

    except IntegrityError:
        return


def _get_today_hh_mm(hh_mm: str) -> datetime:
    hh, mm = map(lambda x: int(x), hh_mm.split(":"))
    naive_datetime = datetime.combine(date=date.today(), time=time(hour=hh, minute=mm))
    return TZ.localize(naive_datetime)
