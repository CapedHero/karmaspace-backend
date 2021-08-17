from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

import pytest

from src.app_auth.models import User
from src.app_auth.tests.values import TEST_EMAIL, TEST_PASSPHRASE, TEST_USERNAME
from src.app_tests.api_clients import get_unauthenticated_api_client


pytestmark = pytest.mark.django_db

VIEW_PATH = reverse("passphrase_login")


class TestPost:
    def test_happy_path(self, mocker):
        # GIVEN
        verify_email_ownership_with_passphrase_mock = mocker.patch(
            "src.app_auth.views.passphrase_login.verify_email_ownership_with_passphrase"
        )
        verify_email_ownership_with_passphrase_mock.return_value = True

        User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)

        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(
            VIEW_PATH, data={"email": TEST_EMAIL, "passphrase": TEST_PASSPHRASE}, format="json"
        )

        # THEN
        assert settings.CSRF_COOKIE_NAME in response.client.cookies
        assert settings.SESSION_COOKIE_NAME in response.client.cookies
        assert response.status_code == HTTP_200_OK

    def test_returns_error_if_required_parameters_are_missing(self):
        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(VIEW_PATH, data={}, format="json")

        # THEN
        expected_response = {
            "email": ["This field is required."],
            "passphrase": ["This field is required."],
        }
        assert response.json() == expected_response
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_returns_403_if_email_ownership_verification_failed(self, mocker):
        # GIVEN
        mocker.patch(
            target="src.app_auth.views.passphrase_login.verify_email_ownership_with_passphrase",
            return_value=False,
        )

        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(
            VIEW_PATH, data={"email": TEST_EMAIL, "passphrase": TEST_PASSPHRASE}, format="json"
        )

        # THEN
        assert response.json() == {"detail": "You do not have permission to perform this action."}
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_returns_403_if_user_with_given_email_does_not_exist(self, mocker):
        # GIVEN
        mocker.patch(
            target="src.app_auth.views.passphrase_login.verify_email_ownership_with_passphrase",
            return_value=True,
        )

        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(
            VIEW_PATH, data={"email": TEST_EMAIL, "passphrase": TEST_PASSPHRASE}, format="json"
        )

        # THEN
        assert response.json() == {"detail": "You do not have permission to perform this action."}
        assert response.status_code == HTTP_403_FORBIDDEN
