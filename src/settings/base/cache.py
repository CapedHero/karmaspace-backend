from .redis import REDIS_URL


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # PickleSerializer is rather unsecure. Yet, Django Response is not
            # JSON serializable. See:
            # + https://github.com/jazzband/django-redis/issues/161
            # + https://github.com/jazzband/django-redis/issues/424
            "SERIALIZER": "django_redis.serializers.pickle.PickleSerializer",
        },
        "KEY_PREFIX": "karmaspace_dj",
    }
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
DJANGO_REDIS_LOGGER = "main"
