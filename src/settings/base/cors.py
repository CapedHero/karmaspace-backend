from django_environ import env


CORS_ORIGIN_WHITELIST = env.list("DJANGO_CORS_ORIGIN_WHITELIST", default=[])
CORS_ALLOW_CREDENTIALS = True
