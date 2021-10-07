from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

import pytest

from src.app_auth.tests.factories import UserFactory
from src.app_auth.tests.values import get_test_gif, TEST_EMAIL, TEST_ID, TEST_USERNAME
from src.app_tests.api_clients import get_authenticated_api_client, get_unauthenticated_api_client


pytestmark = pytest.mark.django_db

VIEW_PATH = reverse("user_me")


class TestGet:
    @pytest.mark.parametrize(
        argnames="avatar", argvalues=[get_test_gif(), None], ids=["with_avatar", "without_avatar"]
    )
    def test_authenticated_user(self, avatar):
        # WHEN
        user = UserFactory(id=TEST_ID, username=TEST_USERNAME, email=TEST_EMAIL, avatar=avatar)
        api_client = get_authenticated_api_client(logged_user=user)
        response = api_client.get(VIEW_PATH)

        # THEN
        assert response.json() == {
            "id": TEST_ID,
            "username": TEST_USERNAME,
            "avatar": f"https://test.com/media/avatars/{user.username}.gif" if avatar else None,
            "is_demo": False,
        }
        assert response.status_code == HTTP_200_OK

    def test_unauthenticated_user(self):
        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.get(VIEW_PATH)

        # THEN
        assert response.json() == {"detail": "Authentication credentials were not provided."}
        assert response.status_code == HTTP_403_FORBIDDEN
