from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from src.app_auth.urls import api_urlpatterns as app_auth_api_urlpatterns
from src.app_auth.urls import auth_urlpatterns
from src.app_auth.urls import emails_urlpatterns as app_auth_emails_urlpatterns
from src.core.views import health_view
from src.karmaspace.urls import api_urlpatterns as karmaspace_api_urlpatterns


api_urlpatterns = [
    *app_auth_api_urlpatterns,
    *karmaspace_api_urlpatterns,
]

emails_urlpatterns = [
    *app_auth_emails_urlpatterns,
]

urlpatterns = [
    path(settings.ADMIN_BASE_PATH, view=admin.site.urls),
    path("api/", include(api_urlpatterns)),
    path("auth/", include(auth_urlpatterns)),
    path("auth/social/", include("social_django.urls", namespace="social")),
    path("health", view=health_view, name="health"),
    path(
        route="favicon.ico",
        view=RedirectView.as_view(url=staticfiles_storage.url("favicon.svg"), permanent=False),
    ),
    re_path(r"^media/(?P<path>.*)$", view=serve, kwargs={"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += [
        path("emails/", include(emails_urlpatterns)),
        path(r"silk/", include("silk.urls", namespace="silk")),
    ]
