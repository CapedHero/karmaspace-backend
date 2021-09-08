from corsheaders.defaults import default_headers

from django_environ import env


CORS_ORIGIN_WHITELIST = env.list("DJANGO_CORS_ORIGIN_WHITELIST", default=[])
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "accept-version",  # unsplash-js sends it
    "cache-control",  # unsplash-js sends it
]
