from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

import pytest

from src.app_auth.models import User
from src.app_auth.tests.factories import UserFactory
from src.app_auth.tests.values import get_test_gif, TEST_EMAIL, TEST_ID, TEST_USERNAME
from src.app_tests.api_clients import get_authenticated_api_client, get_unauthenticated_api_client


pytestmark = pytest.mark.django_db

VIEW_NAME = "user_detail"


class TestGet:
    @pytest.mark.parametrize(
        argnames="avatar", argvalues=[get_test_gif(), None], ids=["with_avatar", "without_avatar"]
    )
    def test_authenticated_user(self, avatar):
        # WHEN
        user = UserFactory(
            id=TEST_ID,
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            avatar=avatar,
        )
        api_client = get_authenticated_api_client(logged_user=user)
        path = reverse(VIEW_NAME, kwargs={"username": user.username})
        response = api_client.get(path)

        # THEN
        assert response.json() == {
            "username": TEST_USERNAME,
            "avatar": f"https://test.com/media/avatars/{user.username}.gif" if avatar else None,
        }
        assert response.status_code == HTTP_200_OK

    def test_unauthenticated_user(self):
        # WHEN
        api_client = get_unauthenticated_api_client()
        path = reverse(VIEW_NAME, kwargs={"username": TEST_USERNAME})
        response = api_client.get(path)

        # THEN
        assert response.json() == {"detail": "Authentication credentials were not provided."}
        assert response.status_code == HTTP_403_FORBIDDEN


class TestPatch:
    def test_happy_path(self):
        # GIVEN
        user = UserFactory(username="FOOBAR")
        path = reverse(VIEW_NAME, kwargs={"username": user.username})
        avatar = get_test_gif()
        updated_username = "FooBar"
        api_client = get_authenticated_api_client(logged_user=user)

        # WHEN
        response = api_client.patch(
            path=path, data={"username": updated_username, "avatar": avatar}
        )

        # THEN
        assert response.json() == {}
        assert response.status_code == HTTP_200_OK

        db_obj = User.objects.get(id=user.id)
        assert db_obj.username == updated_username

    def test_there_are_no_unwanted_side_effects(self):
        # GIVEN
        user = UserFactory()
        path = reverse(VIEW_NAME, kwargs={"username": user.username})
        api_client = get_authenticated_api_client(logged_user=user)

        # WHEN
        response = api_client.patch(path=path, data={}, format="json")

        # THEN
        assert response.json() == {}
        assert response.status_code == HTTP_200_OK

        db_obj = User.objects.get(id=user.id)
        assert db_obj == user

    def test_returns_403_for_not_owner(self):
        # GIVEN
        user_1 = UserFactory()
        user_2 = UserFactory()
        path = reverse(VIEW_NAME, kwargs={"username": user_2.username})
        api_client = get_authenticated_api_client(logged_user=user_1)

        # WHEN
        response = api_client.patch(path)

        # THEN
        assert response.json() == {"detail": "You do not have permission to perform this action."}
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_returns_403_for_unauthenticated_user(self):
        # GIVEN
        user = UserFactory()
        path = reverse(VIEW_NAME, kwargs={"username": user.username})
        api_client = get_unauthenticated_api_client()

        # WHEN
        response = api_client.patch(path)

        # THEN
        assert response.json() == {"detail": "Authentication credentials were not provided."}
        assert response.status_code == HTTP_403_FORBIDDEN
