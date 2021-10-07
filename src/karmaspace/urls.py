from django.urls import path

from .views import (
    demo_view,
    KarmaBoardDetailView,
    KarmaBoardListView,
    KarmaDetailView,
    KarmaListView,
    preview_follow_up_after_joining_email_view,
    preview_thank_you_for_joining_email_view,
    user_feedback_view,
)


api_urlpatterns = [
    path(
        route="demo",
        view=demo_view,
        name="demo",
    ),
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

emails_urlpatterns = [
    path(
        route="preview/follow_up_after_joining",
        view=preview_follow_up_after_joining_email_view,
        name="email_preview_follow_up_after_joining_email",
    ),
    path(
        route="preview/thank_you_for_joining",
        view=preview_thank_you_for_joining_email_view,
        name="email_preview_thank_you_for_joining_email",
    ),
]

msg_urlpatterns = [
    path(
        route="feedback",
        view=user_feedback_view,
        name="user_feedback_msg",
    ),
]
