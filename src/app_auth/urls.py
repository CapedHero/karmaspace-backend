from django.urls import path

from .views import (
    logout_view,
    magic_link_login_view,
    passphrase_login_view,
    passphrase_view,
    preview_passphrase_email_view,
    user_me_view,
    UserDetailView,
    UserListView,
)


auth_urlpatterns = [
    path(route="magic-link/login", view=magic_link_login_view, name="magic_link_login"),
    path(route="passphrase", view=passphrase_view, name="passphrase"),
    path(route="passphrase/login", view=passphrase_login_view, name="passphrase_login"),
    path(route="logout", view=logout_view, name="logout"),
]

api_urlpatterns = [
    path(route="users", view=UserListView.as_view(), name="user_list"),
    path(route="users/<username>", view=UserDetailView.as_view(), name="user_detail"),
    path(route="me", view=user_me_view, name="user_me"),
]

emails_urlpatterns = [
    path(
        route="preview/passphrase",
        view=preview_passphrase_email_view,
        name="emails_preview_passphrase",
    ),
]
