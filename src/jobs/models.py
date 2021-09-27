from django.db import models

from src.core.models import BaseModel
from src.core.utils import get_object_str


class Job(BaseModel):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS"
        DONE = "DONE"

    name = models.CharField(max_length=255)
    marker = models.CharField(max_length=255)
    status = models.CharField(choices=Status.choices, max_length=20)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

        constraints = [
            models.UniqueConstraint(
                fields=["name", "marker"],
                name="unique_job_name_and_marker_combination",
            ),
        ]

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["name", "marker", "status", "id"])

    def __str__(self) -> str:
        return f"Job {self.name}/{self.marker} with status {self.status} | #ID={self.id}"
