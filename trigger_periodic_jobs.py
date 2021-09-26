import json
import time
from uuid import uuid4

from redis import Redis

from django_environ import env


REDIS_URL = f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT')}"
REDIS_CLIENT = Redis.from_url(REDIS_URL)
QUEUE_NAME = "default"


def trigger_periodic_jobs() -> None:
    """
    https://dramatiq.io/advanced.html#enqueueing-messages-from-other-languages
    """
    dramatiq_msg_id = _generate_unique_id()
    redis_msg_id = _generate_unique_id()
    timestamp_in_ms = time.time() * 1_000

    payload = {
        "queue_name": QUEUE_NAME,
        "actor_name": "run_periodic_jobs",
        "args": [],
        "kwargs": {},
        "options": {"redis_message_id": redis_msg_id},
        "message_id": dramatiq_msg_id,
        "message_timestamp": timestamp_in_ms,
    }

    encoded_payload = json.dumps(payload).encode("UTF-8")
    REDIS_CLIENT.hset(f"dramatiq:{QUEUE_NAME}.msgs", key=redis_msg_id, value=encoded_payload)
    REDIS_CLIENT.rpush(f"dramatiq:{QUEUE_NAME}", redis_msg_id)


def _generate_unique_id() -> str:
    return str(uuid4())


if __name__ == "__main__":
    trigger_periodic_jobs()
