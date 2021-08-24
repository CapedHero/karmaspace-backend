from tempfile import NamedTemporaryFile
from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.postgres.fields import CICharField, CIEmailField
from django.core.files import File
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from rest_framework.status import HTTP_200_OK

import requests

from src.core.models import BaseModel
from src.core.utils import get_object_str


# from src.karmaspace.tasks import send_new_user_created_msg_to_karmaspace_team


class UsernameValidator(RegexValidator):
    regex = r"^[a-zA-Z0-9-]{2,}$"
    message = "Accepted characters are lower and uppercase letters, numbers, and hyphen."


def get_avatar_upload_to_path(instance: "User", filename: str) -> str:
    _, file_suffix = filename.rsplit(".", maxsplit=1)
    return f"avatars/{instance.username}.{file_suffix}"


class User(PermissionsMixin, AbstractBaseUser, BaseModel):
    username = CICharField(max_length=50, unique=True, validators=[UsernameValidator()])
    full_name = models.CharField(max_length=50, default="", blank=True)
    email = CIEmailField(unique=True)
    avatar = models.ImageField(upload_to=get_avatar_upload_to_path, null=True, blank=True)

    is_staff = models.BooleanField(
        default=False, help_text="Designates whether the user can log into this admin site."
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    password = models.CharField(max_length=128, blank=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["id", "username", "email"])

    def __str__(self) -> str:
        return f"User {self.username} | #ID={self.id}"

    @property
    def first_name(self) -> str:
        return self.full_name.split(" ")[0]

    @property
    def last_name(self) -> str:
        return self.full_name.split(" ")[-1]

    def save(self, *args: Any, **kwargs: Any) -> None:
        # is_new = not self.id

        super().save(*args, **kwargs)

        # if is_new and settings.ANALYTICS_IS_NEW_USERS_NOTIFICATIONS_ON:
        #     send_new_user_created_msg_to_karmaspace_team.send(self.username, self.email)

    def save_random_avatar(self) -> None:
        avatar_url = (
            "https://avatars.dicebear.com/api/jdenticon/" + get_random_string(length=10) + ".svg"
        )
        response = requests.get(avatar_url)
        if response.status_code == HTTP_200_OK:
            img_temp = NamedTemporaryFile()
            img_temp.write(response.content)
            img_temp.flush()
            self.avatar.save(f"{self.username}.svg", File(img_temp))
