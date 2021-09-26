from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.app_auth.models import User
from src.core.models import BaseModel
from src.core.utils import get_object_str
from .karmaboard import KarmaBoard


class Goal(BaseModel):
    class Timeframe(models.TextChoices):
        DAILY = "DAILY"
        WEEKLY = "WEEKLY"
        MONTHLY = "MONTHLY"

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="goals")
    karmaboard = models.ForeignKey(to=KarmaBoard, on_delete=models.CASCADE, related_name="goals")
    timeframe = models.CharField(choices=Timeframe.choices, max_length=20)
    target_value = models.IntegerField(validators=[MinValueValidator(-99), MaxValueValidator(99)])

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"

    def __repr__(self) -> str:
        return get_object_str(
            self, attrs_to_show=["owner.username", "karmaboard.name", "karmaboard.id", "id"]
        )

    def __str__(self) -> str:
        return (
            f"{self.timeframe} Goal "
            f"of {self.owner.username} "
            f'for KarmaBoard "{self.karmaboard.name}"/{self.karmaboard.id} '
            f"| #ID={self.id}"
        )
