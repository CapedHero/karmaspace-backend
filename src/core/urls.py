from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from src.app_auth.urls import api_urlpatterns as app_auth_api_urlpatterns
from src.app_auth.urls import auth_urlpatterns
from src.app_auth.urls import emails_urlpatterns as app_auth_emails_urlpatterns
from src.core.views import health_view, mixpanel_proxy_view, sentry_proxy_view, unsplash_proxy_view
from src.karmaspace.urls import api_urlpatterns as karmaspace_api_urlpatterns
from src.karmaspace.urls import emails_urlpatterns as karmaspace_emails_urlpatterns
from src.karmaspace.urls import msg_urlpatterns as karmaspace_msg_urlpatterns


api_urlpatterns = [
    *app_auth_api_urlpatterns,
    *karmaspace_api_urlpatterns,
]

msg_urlpatterns = [
    *karmaspace_msg_urlpatterns,
]

emails_urlpatterns = [
    *app_auth_emails_urlpatterns,
    *karmaspace_emails_urlpatterns,
]

urlpatterns = [
    path(settings.ADMIN_BASE_PATH, view=admin.site.urls),
    path("api/", include(api_urlpatterns)),
    path("api/messages/", include(msg_urlpatterns)),
    path("auth/", include(auth_urlpatterns)),
    path("auth/social/", include("social_django.urls", namespace="social")),
    path("health", view=health_view, name="health"),
    path("proxy/mixpanel/<path:api_path>", view=mixpanel_proxy_view, name="mixpanel_proxy"),
    path("proxy/sentry", view=sentry_proxy_view, name="sentry_tunnel"),
    path("proxy/unsplash/<path:api_path>", view=unsplash_proxy_view, name="unsplash_proxy"),
    path(
        route="favicon.ico",
        view=RedirectView.as_view(url=staticfiles_storage.url("favicon.svg"), permanent=False),
    ),
    re_path(r"^media/(?P<path>.*)$", view=serve, kwargs={"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += [
        path("emails/", include(emails_urlpatterns)),
        # path(r"silk/", include("silk.urls", namespace="silk")),
    ]
