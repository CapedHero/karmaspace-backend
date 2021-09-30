from dataclasses import dataclass, field
from unittest.mock import Mock

from rest_framework.status import HTTP_400_BAD_REQUEST

import pytest
from requests import HTTPError

from src.app_auth.social_auth.pipeline import login_with_social_auth, save_avatar
from src.app_auth.tests.factories import UserFactory
from src.app_auth.tests.values import get_test_gif, TEST_USERNAME


DUMMY_USER = object()
TEST_ID = "id-1"
TEST_ACCESS_TOKEN = "T3st-A33e5s-T0K3n"


@dataclass
class FakeStrategy:
    request: object = field(default_factory=object)


@dataclass
class FakeBackend:
    name: str


@dataclass
class FakeResponse:
    status_code: int

    def raise_for_status(self):
        if self.status_code >= HTTP_400_BAD_REQUEST:
            raise HTTPError("", response=self)


class TestLoginWithSocialAuth:
    def test_happy_path(self, mocker):
        # GIVEN
        login_mock = mocker.patch("src.app_auth.social_auth.pipeline.login")
        strategy = FakeStrategy()
        user = DUMMY_USER

        # WHEN
        login_with_social_auth(strategy, FakeBackend(name="facebook"), user)

        # THEN
        login_mock.assert_called_once_with(
            strategy.request, user, "social_core.backends.facebook.FacebookOAuth2"
        )

    def test_no_user(self, mocker):
        login_mock = mocker.patch("src.app_auth.social_auth.pipeline.login")
        login_with_social_auth(FakeStrategy(), FakeBackend(name="facebook"), user=None)
        login_mock.assert_not_called()

    def test_unhandled_backend(self, mocker):
        login_mock = mocker.patch("src.app_auth.social_auth.pipeline.login")

        with pytest.raises(RuntimeError):
            login_with_social_auth(FakeStrategy(), FakeBackend(name="unhandled"), user=DUMMY_USER)

        login_mock.assert_not_called()


class TestSaveAvatar:
    @pytest.mark.django_db
    def test_happy_path(self, mocker):
        # GIVEN
        requests_get_mock = mocker.patch("requests.get")
        avatar = get_test_gif()
        requests_get_mock.return_value = Mock(
            status_code=200,
            content=avatar.file.getvalue(),
            headers={"Content-Type": "image/jpg"},
        )

        response = {"id": TEST_ID, "access_token": TEST_ACCESS_TOKEN}

        user = UserFactory(username=TEST_USERNAME, avatar=None)

        # WHEN
        save_avatar(FakeBackend(name="facebook"), user, response, is_new=True)

        # THEN
        requests_get_mock.assert_called_once_with(
            f"https://graph.facebook.com/{response['id']}/picture",
            params={"type": "large", "access_token": response["access_token"]},
        )
        assert user.avatar.file.name.endswith(TEST_USERNAME + ".jpg")
        assert user.avatar.file.read() == avatar.file.getvalue()

    def test_no_user(self, mocker):
        # GIVEN
        requests_get_mock = mocker.patch("requests.get")
        response = {"id": TEST_ID, "access_token": TEST_ACCESS_TOKEN}

        # WHEN
        save_avatar(FakeBackend(name="facebook"), user=None, response=response, is_new=True)

        # THEN
        requests_get_mock.assert_not_called()

    @pytest.mark.django_db
    def test_user_is_not_new(self, mocker):
        # GIVEN
        requests_get_mock = mocker.patch("requests.get")
        user = UserFactory()
        response = {"id": TEST_ID, "access_token": TEST_ACCESS_TOKEN}

        # WHEN
        save_avatar(FakeBackend(name="facebook"), user, response, is_new=False)

        # THEN
        requests_get_mock.assert_not_called()

    @pytest.mark.django_db
    def test_unhandled_backend(self, mocker):
        # GIVEN
        requests_get_mock = mocker.patch("requests.get")
        user = UserFactory()
        response = {"id": TEST_ID, "access_token": TEST_ACCESS_TOKEN}

        # WHEN
        save_avatar(FakeBackend(name="unhandled"), user, response, is_new=True)

        # THEN
        requests_get_mock.assert_not_called()

    @pytest.mark.django_db
    def test_failed_downloading_facebook_image(self, mocker, caplog, capsys):
        # GIVEN
        requests_get_mock = mocker.patch("requests.get")
        user_picture_response = FakeResponse(status_code=HTTP_400_BAD_REQUEST)
        requests_get_mock.return_value = user_picture_response

        user = UserFactory()
        response = {"id": TEST_ID, "access_token": TEST_ACCESS_TOKEN}

        # WHEN
        save_avatar(FakeBackend(name="facebook"), user, response, is_new=True)

        # THEN
        assert "Failed downloading social auth image." in caplog.text
