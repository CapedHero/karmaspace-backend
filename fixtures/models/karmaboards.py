from typing import Tuple

from src.app_auth.models import User
from src.karmaspace.models import KarmaBoard
from src.karmaspace.models.unsplash_photo import UnsplashPhoto


def create_karmaboards(
    user: User,
    unsplash_photo_1: UnsplashPhoto,
    unsplash_photo_2: UnsplashPhoto,
    unsplash_photo_3: UnsplashPhoto,
) -> Tuple[KarmaBoard, KarmaBoard, KarmaBoard]:
    karmaboard_1 = KarmaBoard.objects.create(
        owner=user,
        name="Obowiązki domowe",
        unsplash_photo=unsplash_photo_1,
    )

    karmaboard_2 = KarmaBoard.objects.create(
        owner=user,
        name="Rośliny i ogród",
        unsplash_photo=unsplash_photo_2,
    )

    karmaboard_3 = KarmaBoard.objects.create(
        owner=user,
        name="KarmaSpace startup",
        unsplash_photo=unsplash_photo_3,
    )

    return karmaboard_1, karmaboard_2, karmaboard_3
