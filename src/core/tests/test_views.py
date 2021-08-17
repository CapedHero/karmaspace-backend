from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from src.app_tests.api_clients import get_unauthenticated_api_client


def test_health_view():
    # WHEN
    api_client = get_unauthenticated_api_client()
    path = reverse("health")
    response = api_client.get(path)

    # THEN
    assert response.json() == {"status": "pass"}
    assert response.status_code == HTTP_200_OK
