import pytest
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from src.app_auth.auth_logic import verify_email_ownership_with_passphrase
from src.app_auth.models import PassphraseRecord
from src.app_auth.tests.values import TEST_DATETIME, TEST_EMAIL, TEST_PASSPHRASE


@pytest.mark.django_db
class TestVerifyEmailOwnershipWithPassphrase:
    @freeze_time(TEST_DATETIME)
    def test_returns_true_if_matching_non_expired_passphrase_record_exists(self):
        # GIVEN
        PassphraseRecord.objects.create(
            email=TEST_EMAIL,
            passphrase=TEST_PASSPHRASE,
            expires_at=TEST_DATETIME + relativedelta(minutes=15),
        )

        # WHEN
        result = verify_email_ownership_with_passphrase(TEST_EMAIL, TEST_PASSPHRASE)

        # THEN
        assert result is True

    def test_returns_false_if_email_and_passphrase_do_not_match(self):
        # WHEN
        result = verify_email_ownership_with_passphrase(TEST_EMAIL, TEST_PASSPHRASE)

        # THEN
        assert result is False

    @freeze_time(TEST_DATETIME)
    def test_returns_false_and_deletes_db_obj_if_passphrase_is_expired(self):
        # GIVEN
        PassphraseRecord.objects.create(
            email=TEST_EMAIL,
            passphrase=TEST_PASSPHRASE,
            expires_at=TEST_DATETIME - relativedelta(minutes=1),
        )

        # WHEN
        result = verify_email_ownership_with_passphrase(TEST_EMAIL, TEST_PASSPHRASE)

        # THEN
        assert result is False
        assert PassphraseRecord.objects.count() == 0
