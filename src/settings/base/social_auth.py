from django_environ import env


SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    # 'src.app_auth.social_auth.pipeline.require_email',
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "src.app_auth.social_auth.pipeline.mark_user_as_newly_created",
    "src.app_auth.social_auth.pipeline.save_avatar",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "src.app_auth.social_auth.pipeline.login_with_social_auth",
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = []  # Overridden in local and prod settings

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ["first_name", "last_name", "full_name"]
SOCIAL_AUTH_USER_FIELD_MAPPING = {"fullname": "full_name"}
SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = "src.app_auth.social_auth.functions.get_cleaned_username"

SOCIAL_AUTH_FACEBOOK_KEY = env("DJANGO_SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = env("DJANGO_SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id, name, email, picture"}
SOCIAL_AUTH_FACEBOOK_AUTH_EXTRA_ARGUMENTS = {"auth_type": "rerequest"}

SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_KEY = env("DJANGO_SOCIAL_AUTH_GOOGLE_KEY")
SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_SECRET = env("DJANGO_SOCIAL_AUTH_GOOGLE_SECRET")
