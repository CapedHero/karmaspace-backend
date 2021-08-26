from django.urls import path

from .views import KarmaListView, KarmaBoardDetailView, KarmaBoardListView


api_urlpatterns = [
    path(route="karmaboards", view=KarmaBoardListView.as_view(), name="karmaboard_list"),
    path(
        route="karmaboards/<owner_username>/<slug>",
        view=KarmaBoardDetailView.as_view(),
        name="karmaboard_detail",
    ),
    path(
        route="karmaboards/<karmaboard_owner_username>/<karmaboard_slug>/karmas",
        view=KarmaListView.as_view(),
        name="karma_list",
    ),
]
