from django.urls import path

from .views import KarmaBoardListView


api_urlpatterns = [
    path(route="karmaboards", view=KarmaBoardListView.as_view(), name="karmaboard_list"),
]
