from datetime import datetime

from django.conf import settings

from loguru import logger
from pytz import timezone

from src.core.dramatiq_actors import dramatiq_actor
from src.core.utils import get_today_hh_mm
from .daily_goals import create_daily_goals_notifications


@dramatiq_actor()
def run_periodic_jobs() -> None:
    logger.info("Periodic tasks triggered.")

    now = datetime.now(timezone(settings.TIME_ZONE))
    t_18_00 = get_today_hh_mm("18:00")
    t_22_00 = get_today_hh_mm("22:00")

    if t_18_00 <= now <= t_22_00:
        logger.info("create_daily_goals_notifications job scheduled.")
        create_daily_goals_notifications.send()
