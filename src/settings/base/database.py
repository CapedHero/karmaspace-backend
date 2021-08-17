from django_environ import env


DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
