from django.db import transaction

from fixtures import models
from src.app_auth.models import User


def create_demo_for_user(user: User) -> None:
    with transaction.atomic():
        photos = models.create_unsplash_photos()

        karmaboards = models.create_karmaboards(user, photos)

        models.create_karmas(karmaboards)
