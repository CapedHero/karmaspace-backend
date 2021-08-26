from typing import Any

from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.text import slugify

from src.app_auth.models import User
from src.core.models import BaseModel
from src.core.utils import get_object_str


class KarmaBoard(BaseModel):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="karmaboards")
    name = CICharField(max_length=30)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = "Karmaboard"
        verbose_name_plural = "Karmaboards"

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_karmaboard_name_per_owner",
            ),
            models.UniqueConstraint(
                fields=["owner", "slug"],
                name="unique_karmaboard_slug_per_owner",
            ),
        ]

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["owner.username", "slug", "id"])

    def __str__(self) -> str:
        return f"KarmaBoard {self.owner.username}/{self.slug} | #ID={self.id}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
