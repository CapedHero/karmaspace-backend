from django.contrib.postgres.fields import CICharField
from django.db import models

from src.app_auth.models import User
from src.core.models import BaseModel
from src.core.utils import get_object_str
from .karmaboard_user import KarmaBoardUser
from .unsplash_photo import UnsplashPhoto


class KarmaBoard(BaseModel):
    class ValueStep(models.TextChoices):
        BY_1 = "BY_1"
        BY_5 = "BY_5"
        BY_10 = "BY_10"
        FIBONACCI = "FIBONACCI"

    name = CICharField(max_length=30)
    value_step = models.CharField(choices=ValueStep.choices, default=ValueStep.BY_1, max_length=20)
    unsplash_photo = models.ForeignKey(
        to=UnsplashPhoto,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="karmaboards",
    )

    class Meta:
        verbose_name = "Karmaboard"
        verbose_name_plural = "Karmaboards"

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["owner.username", "id"])

    def __str__(self) -> str:
        return f"KarmaBoard {self.name} | #ID={self.id}"

    @property
    def owner(self):
        return User.objects.get(
            karmaboarduser__karmaboard=self,
            karmaboarduser__user_role=KarmaBoardUser.UserRole.OWNER,
        )

    @property
    def members(self):
        return User.objects.filter(
            karmaboarduser__karmaboard=self,
            karmaboarduser__user_role=KarmaBoardUser.UserRole.MEMBER,
        )
