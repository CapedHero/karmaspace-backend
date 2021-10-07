from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.core import time_units
from src.core.models import BaseModel
from src.core.utils import get_object_str
from .karmaboard import KarmaBoard


class Karma(BaseModel):
    karmaboard = models.ForeignKey(to=KarmaBoard, on_delete=models.CASCADE, related_name="karmas")
    name = models.CharField(max_length=75)
    value = models.IntegerField(validators=[MinValueValidator(-99), MaxValueValidator(99)])
    duration_in_m = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(time_units.in_m.HOURS_24)],
    )

    class Meta:
        verbose_name = "Karma"
        verbose_name_plural = "Karmas"

    def __repr__(self) -> str:
        return get_object_str(
            self,
            attrs_to_show=[
                "name",
                "value",
                "karmaboard.owner.username",
                "karmaboard.name",
                "id",
            ],
        )

    def __str__(self) -> str:
        return f'Karma "{self.name}" ({self.karmaboard})'
