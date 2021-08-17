import random

from src.app_auth.passphrase import get_passphrase


def test_get_passphrase(mocker):
    # GIVEN
    mocker.patch.object(random, "sample", return_value=["alfa"] * 5)
    words = ["alfa", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india"]

    # WHEN
    passphrase = get_passphrase(words)

    # THEN
    assert passphrase == "alfa-alfa-alfa-alfa-alfa"
