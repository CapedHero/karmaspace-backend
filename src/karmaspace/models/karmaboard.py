from typing import Any

from django.contrib.postgres.fields import CICharField
from django.db import models

from src.app_auth.models import User
from src.core.models import BaseModel
from src.core.utils import get_object_str
from src.karmaspace.logic.sort_index import get_sort_index_for_last_position


class ValueStep(models.TextChoices):
    BY_1 = "BY_1"
    BY_5 = "BY_5"
    BY_10 = "BY_10"
    FIBONACCI = "FIBONACCI"


class KarmaBoard(BaseModel):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="karmaboards")
    name = CICharField(max_length=30)
    value_step = models.CharField(choices=ValueStep.choices, default=ValueStep.BY_1, max_length=20)
    sort_index = models.FloatField(blank=True)

    class Meta:
        verbose_name = "Karmaboard"
        verbose_name_plural = "Karmaboards"

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_karmaboard_name_per_owner",
            ),
        ]

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["owner.username", "id"])

    def __str__(self) -> str:
        return f"KarmaBoard {self.name} | #ID={self.id}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.sort_index:
            self.sort_index = get_sort_index_for_last_position(
                queryset=self.__class__.objects.filter(owner=self.owner)
            )
        super().save(*args, **kwargs)
