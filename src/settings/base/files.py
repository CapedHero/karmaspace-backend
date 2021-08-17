from dirs import DJANGO_ROOT, PROJECT_ROOT
from django_environ import env


DEFAULT_FILE_STORAGE = "src.core.storage.OverwriteFileSystemStorage"

MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", default=PROJECT_ROOT / "media")
MEDIA_URL = env("DJANGO_MEDIA_URL", default="/media/")

STATIC_ROOT = PROJECT_ROOT / "static"
STATICFILES_DIRS = [DJANGO_ROOT / "static"]
STATIC_URL = "/static/"
STATICFILES_STORAGE = env(
    var="DJANGO_STATICFILES_STORAGE",
    default="whitenoise.storage.CompressedManifestStaticFilesStorage",
)
