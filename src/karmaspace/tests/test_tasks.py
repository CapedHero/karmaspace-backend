import pytest

from src.app_auth.tests.values import TEST_EMAIL, TEST_USERNAME
from src.karmaspace.tasks import send_new_user_created_msg_to_karmaspace_team


pytestmark = pytest.mark.django_db


def test_send_new_user_created_msg_to_karmaspace_team(mailoutbox):
    # GIVEN
    user_username = TEST_USERNAME
    user_email = TEST_EMAIL

    # WHEN
    send_new_user_created_msg_to_karmaspace_team(user_username, user_email)

    # THEN
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]

    assert mail.from_email == '"KarmaSpace News" <karmabot@karmaspace.io>'
    assert list(mail.to) == ["news@karmaspace.io"]
    assert mail.subject == f"Nowy użytkownik - {user_username} | {user_email}"
