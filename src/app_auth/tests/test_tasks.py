from django.conf import settings

from ..tasks import send_passphrase_to_user
from .values import TEST_EMAIL, TEST_PASSPHRASE


def test_send_passphrase_to_user(mailoutbox):
    # WHEN
    user_email = TEST_EMAIL
    passphrase = TEST_PASSPHRASE
    send_passphrase_to_user(user_email, passphrase)

    # THEN
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]

    assert mail.from_email == settings.DEFAULT_FROM_EMAIL
    assert list(mail.to) == [user_email]
    assert mail.subject == f"Twoje jednorazowe hasło do KarmaSpace to {passphrase}"

    actual_html = mail.alternatives[0][0]
    actual_plain_msg = mail.body
    for msg in [actual_html, actual_plain_msg]:
        assert "Twoje jednorazowe hasło do KarmaSpace" in msg
        assert passphrase in msg
