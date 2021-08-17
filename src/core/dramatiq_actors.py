import dramatiq


# Time values in milliseconds
ONE_MINUTE = 1_000 * 60
FIFTEEN_MINUTES = ONE_MINUTE * 15


def dramatiq_actor(**kwargs) -> dramatiq.actor:
    """
    Create Dramatiq actor with controllable default middleware kwargs.
    """
    # Set the maximum number of times a task can be retried
    kwargs.setdefault("max_retries", 3)

    # Set the maximum time a task can be in a queue
    kwargs.setdefault("max_age", FIFTEEN_MINUTES)

    # Set the maximum time an actor may run
    kwargs.setdefault("time_limit", ONE_MINUTE)

    return dramatiq.actor(**kwargs)
