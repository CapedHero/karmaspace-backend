from functools import lru_cache, wraps
from typing import Any, Callable, Dict, Tuple

from django.core.cache import cache as redis_cache


def cache_in_memory(fn: Callable) -> Callable:
    """
    Simple, lightweight, unbounded cache. Sometimes called "memoize".

    Copied form Python Source code:
    https://github.com/python/cpython/blob/9a165399aec930f27639dd173426ccc33586662b/Lib/functools.py#L650-L652
    """
    return lru_cache(maxsize=None)(fn)


def cache_in_redis(cache_key_prefix: str, cache_key_expiration_time_s: int) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def cached_fn(*args, **kwargs):
            cache_key = _get_cache_key_for_fn(cache_key_prefix, args, kwargs)

            value = redis_cache.get(cache_key)

            if value is None:
                value = fn(*args, **kwargs)
                redis_cache.set(cache_key, value, cache_key_expiration_time_s)

            return value

        return cached_fn

    return decorator


def _get_cache_key_for_fn(cache_key_prefix: str, args: Tuple[Any], kwargs: Dict[Any, Any]) -> str:
    cache_key_els = [cache_key_prefix]

    if args:
        args_reprs = [repr(arg) for arg in args]
        cache_key_els.append(f"args-{'-'.join(args_reprs)}")

    if kwargs:
        kwargs_reprs = map(lambda entry: f"{entry[0]!r}={entry[1]!r}", kwargs.items())
        cache_key_els.append(f"kwargs-{'-'.join(kwargs_reprs)}")

    cache_key = ":".join(cache_key_els)

    return cache_key
