from datetime import datetime

from django.core.exceptions import ValidationError

import pytest
import pytz
from freezegun import freeze_time

from src.app_auth.models import PassphraseRecord
from src.app_auth.tests.factories import PassphraseRecordFactory
from src.app_auth.tests.values import TEST_DATETIME, TEST_EMAIL, TEST_PASSPHRASE


pytestmark = pytest.mark.django_db


@freeze_time("2020-01-02 03:45")
def test_instance_is_saved_correctly_in_db():
    # WHEN
    PassphraseRecord.objects.create(
        email=TEST_EMAIL, passphrase=TEST_PASSPHRASE, expires_at=TEST_DATETIME
    )

    # THEN
    assert PassphraseRecord.objects.count() == 1

    db_obj = PassphraseRecord.objects.first()
    assert db_obj.email == TEST_EMAIL
    assert db_obj.passphrase == TEST_PASSPHRASE
    assert db_obj.expires_at == TEST_DATETIME
    assert db_obj.created_at == datetime(2020, 1, 2, 3, 45, tzinfo=pytz.timezone("utc"))
    assert db_obj.modified_at == datetime(2020, 1, 2, 3, 45, tzinfo=pytz.timezone("utc"))


def test_email_is_unique():
    # GIVEN
    PassphraseRecordFactory(email=TEST_EMAIL)

    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        PassphraseRecordFactory(email=TEST_EMAIL)


def test_passphrase_cant_be_null():
    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        PassphraseRecordFactory(passphrase=None)


def test_passphrase_cant_be_empty():
    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        PassphraseRecordFactory(passphrase="")


def test_expires_at_cant_be_null():
    # THEN
    with pytest.raises(ValidationError):
        # WHEN
        PassphraseRecordFactory(expires_at=None)
