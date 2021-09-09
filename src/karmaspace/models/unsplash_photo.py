from django.db import models

from src.core.models import BaseModel
from src.core.utils import get_object_str


class UnsplashPhoto(BaseModel):
    id = models.CharField(primary_key=True, max_length=50)
    regular_url = models.URLField(max_length=500)
    small_url = models.URLField(max_length=500)
    author_name = models.CharField(max_length=100)
    author_url = models.URLField()

    class Meta:
        verbose_name = "Unsplash Photo"
        verbose_name_plural = "Unsplash Photos"

    def __repr__(self) -> str:
        return get_object_str(self, attrs_to_show=["id", "author_name"])

    def __str__(self) -> str:
        return f"Unsplash Photo by {self.author_name} | #ID={self.id}"
