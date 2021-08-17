import factory
from factory.django import DjangoModelFactory

from ..models import PassphraseRecord, User
from .values import TEST_DATETIME, TEST_EMAIL, TEST_PASSPHRASE


class PassphraseRecordFactory(DjangoModelFactory):
    email = TEST_EMAIL
    passphrase = TEST_PASSPHRASE
    expires_at = TEST_DATETIME

    class Meta:
        model = PassphraseRecord


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user-{n}")
    email = factory.LazyAttribute(lambda obj: obj.username + "@test.com")

    class Meta:
        model = User
