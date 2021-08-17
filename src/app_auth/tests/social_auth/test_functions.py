import pytest

from src.app_auth.social_auth.functions import get_cleaned_username


@pytest.mark.parametrize(
    argnames=["input_", "expected_cleaned_username"],
    argvalues=[
        pytest.param("Jan Kowalski", "Jan-Kowalski", id="ascii"),
        pytest.param("Maciej Wrześniewski", "Maciej-Wrzesniewski", id="diacritics"),
        pytest.param("Foo!@#$%^&*()", "Foo", id="special-symbols"),
        pytest.param("Foo   Bar---Baz", "Foo-Bar-Baz", id="non-normalized-spacing"),
    ],
)
def test_get_cleaned_username(input_, expected_cleaned_username):
    actual_cleaned_username = get_cleaned_username(input_)
    assert actual_cleaned_username == expected_cleaned_username
