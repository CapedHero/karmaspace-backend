from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

import pytest

from src.app_tests.api_clients import get_authenticated_api_client, get_unauthenticated_api_client


pytestmark = pytest.mark.django_db

VIEW_PATH = reverse("logout")


class TestPost:
    def test_authenticated_user(self, mocker):
        # WHEN
        logout_mock = mocker.patch("src.app_auth.views.logout.logout")
        api_client = get_authenticated_api_client()
        response = api_client.post(VIEW_PATH)

        # THEN
        assert response.json() == {}
        assert response.status_code == HTTP_200_OK

        logout_mock.assert_called_once()

    def test_unauthenticated_user(self, mocker):
        # WHEN
        logout_mock = mocker.patch("src.app_auth.views.logout.logout")
        api_client = get_unauthenticated_api_client()
        response = api_client.post(VIEW_PATH)

        # THEN
        assert response.json() == {}
        assert response.status_code == HTTP_200_OK

        logout_mock.assert_called_once()
