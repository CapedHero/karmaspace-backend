import logging
from datetime import date

from django.db import IntegrityError, transaction
from django.db.models import IntegerField, OuterRef, Q, QuerySet, Subquery
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce

from src.core.dramatiq_actors import dramatiq_actor
from src.core.utils import get_today_hh_mm
from src.karmaspace.models import Goal, KarmaBoard
from src.notifications.models import Notification
from ..models import Job


logger = logging.getLogger("main")

JOB_NAME = "create_daily_goals_notifications"


@dramatiq_actor()
def create_daily_goals_notifications() -> None:
    if _is_job_already_handled():
        return

    try:
        with transaction.atomic():
            job = Job(name=JOB_NAME, marker=str(date.today()))

            job.status = Job.Status.IN_PROGRESS
            job.save()

            daily_goals = _get_daily_goals()

            for goal in daily_goals:
                if goal.today_total_karmas_value < goal.target_value:
                    _create_daily_goal_notification(goal)

            job.status = Job.Status.DONE
            job.save()

    except IntegrityError:
        return


def _is_job_already_handled() -> bool:
    return Job.objects.filter(name=JOB_NAME, marker=str(date.today())).exists()


def _get_daily_goals() -> QuerySet[Goal]:
    today_midnight = get_today_hh_mm("00:00")

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

    return daily_goals


def _create_daily_goal_notification(goal: Goal) -> None:
    Notification.objects.create(
        owner=goal.owner,
        type=Notification.Type.GOAL,
        content=(
            f'KarmaBoard "{goal.karmaboard.name}": Brakuje Ci '
            f"{goal.target_value - goal.today_total_karmas_value} "
            f"Punktów Karmy do zrealizowania dziennego celu 🏁"
        ),
    )
