from django.conf import settings

import pytest

from ..tasks import send_passphrase_to_user
from .values import TEST_EMAIL, TEST_PASSPHRASE, TEST_URL


@pytest.mark.django_db
def test_send_passphrase_to_user(mailoutbox):
    # WHEN
    user_email = TEST_EMAIL
    passphrase = TEST_PASSPHRASE
    send_passphrase_to_user(user_email, passphrase, redirect_url=TEST_URL)

    # THEN
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]

    assert mail.from_email == settings.DEFAULT_FROM_EMAIL
    assert list(mail.to) == [user_email]
    assert mail.subject == "Logowanie do KarmaSpace"

    actual_html = mail.alternatives[0][0]
    actual_plain_msg = mail.body
    for msg in [actual_html, actual_plain_msg]:
        assert "wykorzystaj swoje tymczasowe hasło" in msg
        assert passphrase in msg
