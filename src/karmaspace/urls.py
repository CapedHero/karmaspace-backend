from django.urls import path

from .views import (
    KarmaBoardDetailView,
    KarmaBoardListView,
    KarmaDetailView,
    KarmaListView,
    user_feedback_view,
)


api_urlpatterns = [
    path(
        route="karmaboards",
        view=KarmaBoardListView.as_view(),
        name="karmaboard_list",
    ),
    path(
        route="karmaboards/<uuid:pk>",
        view=KarmaBoardDetailView.as_view(),
        name="karmaboard_detail",
    ),
    path(
        route="karmaboards/<uuid:karmaboard_pk>/karmas",
        view=KarmaListView.as_view(),
        name="karma_list",
    ),
    path(
        route="karmas/<uuid:pk>",
        view=KarmaDetailView.as_view(),
        name="karma_detail",
    ),
]

msg_urlpatterns = [
    path(
        route="feedback",
        view=user_feedback_view,
        name="user_feedback_msg",
    ),
]
