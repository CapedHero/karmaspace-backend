from rest_framework.test import APIClient

from src.app_auth.tests.factories import UserFactory


def get_unauthenticated_api_client():
    return APIClient()


def get_authenticated_api_client(*, logged_user=None):
    if logged_user is None:
        logged_user = UserFactory()
    api_client = APIClient()
    api_client.force_authenticate(user=logged_user)
    return api_client
