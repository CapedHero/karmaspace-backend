from datetime import datetime

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

import pytest
import pytz
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from src.app_auth.models import PassphraseRecord
from src.app_auth.tests.values import TEST_DATETIME, TEST_EMAIL, TEST_PASSPHRASE, TEST_URL
from src.app_tests.api_clients import get_unauthenticated_api_client


pytestmark = pytest.mark.django_db


VIEW_PATH = reverse("passphrase")


class TestPost:
    @freeze_time(TEST_DATETIME)
    def test_happy_path(self, mocker):
        # GIVEN
        PassphraseRecord.objects.create(
            email=TEST_EMAIL,
            passphrase="this-passphrase-should-be-deleted",
            expires_at=datetime(2000, 1, 2, 3, 4, 5, tzinfo=pytz.timezone("utc")),
        )
        mocker.patch("src.app_auth.views.passphrase.get_passphrase", return_value=TEST_PASSPHRASE)
        send_passphrase_to_user_mock = mocker.patch(
            "src.app_auth.views.passphrase.send_passphrase_to_user"
        )

        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(
            path=VIEW_PATH,
            data={"email": TEST_EMAIL, "redirect_url": TEST_URL},
            format="json",
        )

        # THEN
        assert response.json() == {}
        assert response.status_code == HTTP_201_CREATED

        assert PassphraseRecord.objects.count() == 1
        db_obj = PassphraseRecord.objects.first()
        assert db_obj.email == TEST_EMAIL
        assert db_obj.passphrase == TEST_PASSPHRASE
        assert db_obj.expires_at == TEST_DATETIME + relativedelta(minutes=15)

        send_passphrase_to_user_mock.send.assert_called_once_with(
            TEST_EMAIL,
            TEST_PASSPHRASE,
            TEST_URL,
        )

    def test_returns_error_if_email_is_missing(self):
        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(VIEW_PATH, data={}, format="json")

        # THEN
        assert response.json() == {"email": ["This field is required."]}
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_returns_error_if_email_has_invalid_format(self):
        # WHEN
        api_client = get_unauthenticated_api_client()
        response = api_client.post(
            VIEW_PATH, data={"email": "email-with-invalid-format"}, format="json"
        )

        # THEN
        assert response.json() == {"email": ["Enter a valid email address."]}
        assert response.status_code == HTTP_400_BAD_REQUEST
