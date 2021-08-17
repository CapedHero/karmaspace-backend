from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

import pytest

from src.app_auth.models import User
from src.app_auth.tests.factories import UserFactory
from src.app_auth.tests.values import TEST_EMAIL, TEST_ID, TEST_PASSPHRASE, TEST_USERNAME
from src.app_tests.api_clients import get_authenticated_api_client, get_unauthenticated_api_client


pytestmark = pytest.mark.django_db

VIEW_PATH = reverse("user_list")


class TestPost:
    def test_happy_path(self, mocker):
        # GIVEN
        verify_email_ownership_with_passphrase_mock = mocker.patch(
            target="src.app_auth.views.user_list.verify_email_ownership_with_passphrase",
            return_value=True,
        )
        save_random_avatar_mock = mocker.patch.object(User, "save_random_avatar")
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.post(
            path=VIEW_PATH,
            data={"email": TEST_EMAIL, "username": TEST_USERNAME, "passphrase": TEST_PASSPHRASE},
            format="json",
        )

        # THEN
        assert response.json() == {}
        assert response.status_code == HTTP_201_CREATED

        verify_email_ownership_with_passphrase_mock.assert_called_once_with(
            TEST_EMAIL, TEST_PASSPHRASE
        )
        save_random_avatar_mock.assert_called_once_with()

        db_objects = User.objects.all()
        assert len(db_objects) == 1

        db_obj = db_objects[0]
        assert db_obj.email == TEST_EMAIL
        assert db_obj.username == TEST_USERNAME

    def test_provided_user_email_must_be_unique(self):
        # GIVEN
        api_client = get_authenticated_api_client()
        UserFactory(email=TEST_EMAIL)

        # WHEN
        response = api_client.post(
            path=VIEW_PATH,
            data={"email": TEST_EMAIL, "username": TEST_USERNAME, "passphrase": TEST_PASSPHRASE},
            format="json",
        )

        # THEN
        assert response.json() == {"email": ["This field must be unique."]}
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_provided_username_must_be_unique(self):
        # GIVEN
        api_client = get_authenticated_api_client()
        UserFactory(username=TEST_USERNAME)

        # WHEN
        response = api_client.post(
            path=VIEW_PATH,
            data={"email": TEST_EMAIL, "username": TEST_USERNAME, "passphrase": TEST_PASSPHRASE},
            format="json",
        )

        # THEN
        assert response.json() == {"username": ["This field must be unique."]}
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_returns_error_if_required_parameters_are_missing(self):
        # GIVEN
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.post(path=VIEW_PATH, data={}, format="json")

        # THEN
        expected_response = {
            "email": ["This field is required."],
            "passphrase": ["This field is required."],
            "username": ["This field is required."],
        }
        assert response.json() == expected_response
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_returns_403_if_email_ownership_verification_failed(self, mocker):
        # GIVEN
        mocker.patch(
            target="src.app_auth.views.user_list.verify_email_ownership_with_passphrase",
            return_value=False,
        )

        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(
            path=VIEW_PATH,
            data={"email": TEST_EMAIL, "username": TEST_USERNAME, "passphrase": TEST_PASSPHRASE},
            format="json",
        )

        # THEN
        assert response.json() == {"detail": "You do not have permission to perform this action."}
        assert response.status_code == HTTP_403_FORBIDDEN


class TestHead:
    def test_with_email_query_param_returns_200_if_user_exists(self):
        # GIVEN
        UserFactory()
        UserFactory(id=TEST_ID, username=TEST_USERNAME, email=TEST_EMAIL)
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.head(VIEW_PATH + "?" + f"email={TEST_EMAIL}")

        # THEN
        assert response.status_code == HTTP_200_OK

    def test_with_email_query_param_returns_404_if_user_does_not_exist(self):
        # GIVEN
        UserFactory()
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.head(VIEW_PATH + "?" + f"email={TEST_EMAIL}")

        # THEN
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_with_email_username_param_returns_200_if_user_exists(self):
        # GIVEN
        UserFactory()
        UserFactory(id=TEST_ID, username=TEST_USERNAME, email=TEST_EMAIL)
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.head(VIEW_PATH + "?" + f"username={TEST_USERNAME}")

        # THEN
        assert response.status_code == HTTP_200_OK

    def test_with_username_query_param_returns_404_if_user_does_not_exist(self):
        # GIVEN
        UserFactory()
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.head(VIEW_PATH + "?" + f"username={TEST_USERNAME}")

        # THEN
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_without_email_or_username_query_param_returns_400(self):
        # GIVEN
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.head(VIEW_PATH)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_with_both_email_and_username_query_param_returns_400(self):
        # GIVEN
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.head(VIEW_PATH + "?email=foo&username=bar")

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
