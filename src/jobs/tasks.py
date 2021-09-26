from datetime import datetime

from django.db.models import IntegerField, OuterRef, Q, Subquery
from django.db.models.aggregates import Sum

from pytz import timezone

from src.core.dramatiq_actors import dramatiq_actor
from src.karmaspace.models import Goal, KarmaBoard, Notification


@dramatiq_actor()
def run_periodic_jobs() -> None:
    now = datetime.now(timezone("Europe/Warsaw"))

    if _is_6pm(now):
        create_daily_goals_notifications.send()
        print("It truly is 6 PM!")  # noqa: T001

    print("Periodic tasks triggered.")  # noqa: T001


def _is_6pm(timestamp: datetime) -> bool:
    return _is_hh_mm(timestamp, "16:47")


def _is_hh_mm(timestamp: datetime, hh_mm: str) -> bool:
    hh, mm = map(lambda x: int(x), hh_mm.split(":"))
    return timestamp.hour == hh and timestamp.minute == mm


@dramatiq_actor()
def create_daily_goals_notifications() -> None:
    now = datetime.now(timezone("Europe/Warsaw"))
    today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    today_karmas_per_karmaboard = KarmaBoard.objects.filter(
        id=OuterRef("karmaboard__id"),
    ).annotate(
        today_karmas_total_value=Sum(
            "karmas__value",
            filter=Q(karmas__created_at__gte=today_midnight),
        ),
    )
    daily_goals = Goal.objects.filter(timeframe=Goal.Timeframe.DAILY).annotate(
        today_total_karmas_value=Subquery(
            queryset=today_karmas_per_karmaboard.values("today_karmas_total_value"),
            output_field=IntegerField(),
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
