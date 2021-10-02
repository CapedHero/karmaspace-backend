from datetime import datetime

from django.conf import settings

from loguru import logger
from pytz import timezone

from src.core.dramatiq_actors import dramatiq_actor
from src.core.utils import get_today_hh_mm
from .daily_goals import create_daily_goals_notifications
from .onboarding import send_follow_up_email_after_joining


@dramatiq_actor()
def run_periodic_jobs() -> None:
    logger.info("Periodic jobs triggered.")

    now = datetime.now(timezone(settings.TIME_ZONE))
    t_17_00 = get_today_hh_mm("17:00")
    t_22_00 = get_today_hh_mm("22:00")

    if t_17_00 <= now <= t_22_00:
        create_daily_goals_notifications.send()
        logger.info("create_daily_goals_notifications job scheduled.")

        send_follow_up_email_after_joining.send()
        logger.info("send_follow_up_email_after_joining job scheduled.")
