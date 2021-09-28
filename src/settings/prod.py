from loguru import logger

from django_environ import env
from .base import *


# Can be generated with:
# echo $(base64 /dev/urandom | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c32)
ADMIN_BASE_PATH = env("DJANGO_ADMIN_BASE_PATH")

RENDER_EXTERNAL_HOSTNAME = env("RENDER_EXTERNAL_HOSTNAME", default="")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = env.list(
    "DJANGO_SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS", default=[]
)

#########
# FILES #
#########

DEFAULT_FILE_STORAGE = "src.core.storage.MediaRootS3Boto3Storage"

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {
    "ACL": "public-read",
}
AWS_QUERYSTRING_AUTH = False

#############
# ANALYTICS #
#############

ANALYTICS_IS_NEW_USERS_NOTIFICATIONS_ON = True

###########
# LOGGING #
###########

logger.add(sys.stderr, serialize=True)
