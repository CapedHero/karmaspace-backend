from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile

import pytz


TEST_BOOL = True
TEST_COOKBOOK_NAME = "Cookbook Foo"
TEST_DATETIME = datetime(2020, 1, 2, 3, 45, tzinfo=pytz.timezone("utc"))
TEST_EMAIL = "foo@bar.baz"
TEST_FULL_NAME = "Foo Bar"
TEST_ID = 123
TEST_PASSPHRASE = "foo-bar-baz"
TEST_USERNAME = "user-foo"


def get_test_gif(name: str = "test.gif") -> SimpleUploadedFile:
    return SimpleUploadedFile(
        name=name,
        content=(
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        ),
        content_type="image/gif",
    )
