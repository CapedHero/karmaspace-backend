from django.urls import path

from .views import KarmaBoardDetailView, KarmaBoardListView, KarmaDetailView, KarmaListView


api_urlpatterns = [
    path(
        route="karmaboards",
        view=KarmaBoardListView.as_view(),
        name="karmaboard_list",
    ),
    path(
        route="karmaboards/<owner_username>/<slug>",
        view=KarmaBoardDetailView.as_view(),
        name="karmaboard_detail",
    ),
    path(
        route="karmaboards/<owner_username>/<slug>/karmas",
        view=KarmaListView.as_view(),
        name="karma_list",
    ),
    path(
        route="karmas/<id_>",
        view=KarmaDetailView.as_view(),
        name="karma_detail",
    ),
]
