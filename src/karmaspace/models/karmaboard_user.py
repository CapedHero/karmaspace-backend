from typing import Any

from django.db import models

from src.app_auth.models import User
from src.core.models import BaseModel
from src.core.utils import get_object_str
from ..logic.sort_index import get_sort_index_for_last_position


class KarmaBoardUser(BaseModel):
    class UserRole(models.TextChoices):
        OWNER = "OWNER"
        MEMBER = "MEMBER"

    karmaboard = models.ForeignKey(to="KarmaBoard", on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    user_role = models.CharField(choices=UserRole.choices, max_length=20)
    sort_index = models.FloatField(blank=True)

    class Meta:
        verbose_name = "Karmaboard User"
        verbose_name_plural = "Karmaboards Users"

        constraints = [
            models.UniqueConstraint(
                fields=["karmaboard", "user"],
                name="unique_karmaboard_user_combination",
            ),
        ]

    def __repr__(self) -> str:
        return get_object_str(
            self,
            attrs_to_show=["karmaboard.name", "user.username", "id"],
        )

    def __str__(self) -> str:
        return f"KarmaBoardUser {self.karmaboard.name}-{self.user.username} | #ID={self.id}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.sort_index:
            self.sort_index = get_sort_index_for_last_position(
                queryset=self.__class__.objects.filter(user=self.user)
            )
        super().save(*args, **kwargs)
