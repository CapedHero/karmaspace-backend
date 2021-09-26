from django_environ import env


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("DJANGO_EMAIL_HOST")
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("DJANGO_EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_ALLOWED_HTML_TAGS = [
    "a",
    "b",
    "blockquote",
    "em",
    "i",
    "li",
    "ol",
    "p",
    "strong",
    "ul",
]


DEFAULT_FROM_EMAIL = env("DJANGO_EMAIL_DEFAULT_FROM_EMAIL")
