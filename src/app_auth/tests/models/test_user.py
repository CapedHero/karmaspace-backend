from datetime import datetime
from unittest.mock import Mock

from django.core.exceptions import ValidationError

import pytest
import pytz
from freezegun import freeze_time

from src.app_auth.models import get_avatar_upload_to_path, User
from src.app_auth.tests.factories import UserFactory
from src.app_auth.tests.values import (
    get_test_gif,
    TEST_BOOL,
    TEST_EMAIL,
    TEST_FULL_NAME,
    TEST_USERNAME,
)


pytestmark = pytest.mark.django_db


@freeze_time("2020-01-02 03:45")
def test_instance_is_saved_correctly_in_db():
    # WHEN
    avatar = get_test_gif(name="test-saving-user-model.gif")

    user = User.objects.create(
        username=TEST_USERNAME,
        full_name=TEST_FULL_NAME,
        email=TEST_EMAIL,
        avatar=avatar,
        is_staff=TEST_BOOL,
        is_active=TEST_BOOL,
    )

    # THEN
    assert User.objects.count() == 1

    db_obj = User.objects.get(id=user.id)
    assert db_obj.username == TEST_USERNAME
    assert db_obj.full_name == TEST_FULL_NAME
    assert db_obj.email == TEST_EMAIL
    assert db_obj.avatar.file.read() == avatar.file.getvalue()
    assert db_obj.is_staff == TEST_BOOL
    assert db_obj.is_active == TEST_BOOL
    assert db_obj.created_at == datetime(2020, 1, 2, 3, 45, tzinfo=pytz.timezone("utc"))
    assert db_obj.modified_at == datetime(2020, 1, 2, 3, 45, tzinfo=pytz.timezone("utc"))


def test_defaults():
    # WHEN
    user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)

    # THEN
    db_obj = User.objects.get(id=user.id)
    assert db_obj.full_name == ""
    assert db_obj.avatar.name == ""
    assert db_obj.is_staff is False
    assert db_obj.is_active is True


@pytest.mark.parametrize(
    argnames="username",
    argvalues=["foobar123", "Foo-Bar-123"],
    ids=lambda value: f'username="{value}"',
)
def test_valid_username(username):
    # WHEN
    UserFactory(username=username)

    # THEN no exception was raised.


@pytest.mark.parametrize(
    argnames="username", argvalues=["", "a", "!@#$%^&*()"], ids=lambda value: f'username="{value}"'
)
def test_invalid_username(username):
    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        UserFactory(username=username)


def test_username_is_case_insensitive_unique():
    # GIVEN
    UserFactory(username=TEST_USERNAME.lower())

    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        UserFactory(username=TEST_USERNAME.upper())


def test_email_is_unique():
    # GIVEN
    UserFactory(email=TEST_EMAIL)

    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        UserFactory(username=TEST_EMAIL)


def test_username_cant_exceed_50_chars():
    # WHEN 1
    UserFactory(username="".join("a" for _ in range(50)))
    # THEN 1 - no exception is raised

    # THEN 2
    with pytest.raises(ValidationError):
        # WHEN 2
        UserFactory(username="".join("a" for _ in range(51)))


def test_full_name_cant_exceed_100_chars():
    # WHEN 1
    UserFactory(full_name="".join("a" for _ in range(50)))
    # THEN 1 - no exception is raised

    # THEN 2
    with pytest.raises(ValidationError):
        # WHEN 2
        UserFactory(full_name="".join("a" for _ in range(51)))


def test_first_name():
    # WHEN
    user = UserFactory(full_name="Foo Bar Baz")

    # THEN
    assert user.first_name == "Foo"


def test_last_name():
    # WHEN
    user = UserFactory(full_name="Foo Bar Baz")

    # THEN
    assert user.last_name == "Baz"


def test_save_random_avatar(mocker):
    # GIVEN
    random_string = "random_string"

    requests_get_mock = mocker.patch("requests.get")
    mocker.patch(target="src.app_auth.models.user.get_random_string", return_value="random_string")

    avatar = get_test_gif()
    requests_get_mock.return_value = Mock(status_code=200, content=avatar.file.getvalue())

    # WHEN
    user = UserFactory(username=TEST_USERNAME)
    user.save_random_avatar()

    # THEN
    requests_get_mock.assert_called_once_with(
        "https://avatars.dicebear.com/api/jdenticon/" + random_string + ".svg"
    )
    assert user.avatar.file.name.endswith(TEST_USERNAME + ".svg")
    assert user.avatar.file.read() == avatar.file.getvalue()


@pytest.mark.parametrize(
    argnames="filename",
    argvalues=[
        pytest.param("foo.png", id="png-file"),
        pytest.param("bar.svg", id="svg-file"),
    ],
)
def test_get_avatar_upload_to_path(filename: str):
    # GIVEN
    user = UserFactory()

    # WHEN
    path = get_avatar_upload_to_path(user, filename)

    # THEN
    _, file_suffix = filename.rsplit(".", maxsplit=1)
    assert path == f"avatars/{user.username}.{file_suffix}"


# class TestKarmaSpaceTeamIsMessagedAboutNewUserCreation:
#     @pytest.mark.parametrize(
#         argnames="is_notification_on",
#         argvalues=[
#             pytest.param(True, id="notification_is_enabled"),
#             pytest.param(False, id="notification_is_disabled"),
#         ],
#     )
#     def test_user_created(self, is_notification_on, mocker, settings):
#         # GIVEN
#         settings.ANALYTICS_IS_NEW_USERS_NOTIFICATIONS_ON = is_notification_on
#         send_new_user_created_msg_to_karmaspace_team_mock = mocker.patch(
#             "src.app_auth.models.user.send_new_user_created_msg_to_karmaspace_team"
#         )
#
#         # WHEN
#         user = UserFactory()
#
#         # THEN
#         if is_notification_on:
#             send_new_user_created_msg_to_karmaspace_team_mock.send.assert_called_once_with(
#                 user.username, user.email
#             )
#         else:
#             send_new_user_created_msg_to_karmaspace_team_mock.send.assert_not_called()
#
#     @pytest.mark.parametrize(
#         argnames="is_notification_on",
#         argvalues=[
#             pytest.param(True, id="notification_is_enabled"),
#             pytest.param(False, id="notification_is_disabled"),
#         ],
#     )
#     def test_user_updated(self, is_notification_on, mocker, settings):
#         # GIVEN
#         send_new_user_created_msg_to_karmaspace_team_mock = mocker.patch(
#             "src.app_auth.models.user.send_new_user_created_msg_to_karmaspace_team"
#         )
#
#         settings.ANALYTICS_IS_NEW_USERS_NOTIFICATIONS_ON = False
#         user = UserFactory(full_name="foo")
#
#         settings.ANALYTICS_IS_NEW_USERS_NOTIFICATIONS_ON = is_notification_on
#
#         # WHEN
#         user.full_name = "bar"
#         user.save()
#
#         # THEN
#         send_new_user_created_msg_to_karmaspace_team_mock.send.assert_not_called()
