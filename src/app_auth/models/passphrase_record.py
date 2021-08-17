from typing import Any

from django.db import models

from src.core.models import BaseModel
from src.core.utils import get_object_str


class PassphraseRecord(BaseModel):
    email = models.EmailField(unique=True)
    passphrase = models.CharField(max_length=50)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Passphrase Record"
        verbose_name_plural = "Passphrase Records"

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["id", "email", "expires_at"])

    def __str__(self) -> str:
        return f"PassphraseRecord email={self.email}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
