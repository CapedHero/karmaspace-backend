from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from src.app_tests.api_clients import get_unauthenticated_api_client


class TestEmailsPreviewPassphrase:
    VIEW_PATH = reverse("emails_preview_passphrase")

    def test_get(self):
        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.get(self.VIEW_PATH)

        # THEN
        response_html = response.content.decode()
        assert "tymczasowe hasło" in response_html
        assert "dummy-passphrase-foo-bar" in response_html
        assert "15 minut" in response_html
        assert response.status_code == HTTP_200_OK
