from django.urls import path

from .views import KarmaBoardDetailView, KarmaBoardListView


api_urlpatterns = [
    path(route="karmaboards", view=KarmaBoardListView.as_view(), name="karmaboard_list"),
    path(
        route="karmaboards/<owner_username>/<slug>",
        view=KarmaBoardDetailView.as_view(),
        name="karmaboard_detail",
    ),
]
