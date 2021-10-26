from typing import Any

from django.db import models

from src.core.models import BaseModel
from src.core.utils import create_random_string, get_object_str


class KarmaBoardInvitation(BaseModel):
    karmaboard = models.ForeignKey(
        to="KarmaBoard",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    secret = models.CharField(max_length=50)

    class Meta:
        verbose_name = "KarmaBoard Invitation"
        verbose_name_plural = "KarmaBoards Invitations"

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["id", "karmaboard.id", "karmaboard.name"])

    def __str__(self) -> str:
        return f"KarmaBoardInvitation id={self.id} for KarmaBoard id={self.karmaboard.id}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.created_at:
            self.secret = create_random_string(chars_num=30)  # ~ 141 bits of entropy
        super().save(*args, **kwargs)
