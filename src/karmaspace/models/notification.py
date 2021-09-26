from django.db import models

from src.app_auth.models import User
from src.core.models import BaseModel
from src.core.utils import get_object_str


class Notification(BaseModel):
    class Type(models.TextChoices):
        GOAL = "GOAL"

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(choices=Type.choices, max_length=20)
    content = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["owner.username", "id"])

    def __str__(self) -> str:
        return f"Notification for {self.owner.username} | #ID={self.id}"
