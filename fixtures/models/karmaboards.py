from dataclasses import dataclass

from fixtures.models.unsplash_photos import Photos
from src.app_auth.models import User
from src.karmaspace.models import KarmaBoard


@dataclass
class KarmaBoards:
    duties_and_leasure: KarmaBoard
    family_relations: KarmaBoard
    fitness_and_health: KarmaBoard
    house_chores: KarmaBoard
    learning_english: KarmaBoard
    learning_guitar: KarmaBoard
    plants: KarmaBoard
    reading_books: KarmaBoard


def create_karmaboards(user: User, photos: Photos) -> KarmaBoards:
    karmaboards = KarmaBoards(
        duties_and_leasure=KarmaBoard.objects.create(
            owner=user,
            name="Obowiązki i rozrywki Hani",
            unsplash_photo=photos.sunflowers,
            sort_index=0.1,
        ),
        family_relations=KarmaBoard.objects.create(
            owner=user,
            name="Relacje rodzinne",
            unsplash_photo=photos.family,
            sort_index=0.8,
        ),
        fitness_and_health=KarmaBoard.objects.create(
            owner=user,
            name="Sport i zdrowie",
            unsplash_photo=photos.bowl_food,
            sort_index=0.3,
        ),
        house_chores=KarmaBoard.objects.create(
            owner=user,
            name="Dom i porządki",
            unsplash_photo=photos.wooden_house,
            sort_index=0.2,
        ),
        learning_english=KarmaBoard.objects.create(
            owner=user,
            name="Nauka angielskiego",
            unsplash_photo=photos.english_flag,
            sort_index=0.5,
        ),
        learning_guitar=KarmaBoard.objects.create(
            owner=user,
            name="Gitara",
            unsplash_photo=photos.guitar,
            sort_index=0.6,
        ),
        plants=KarmaBoard.objects.create(
            owner=user,
            name="Rośliny",
            unsplash_photo=photos.succulents,
            sort_index=0.4,
        ),
        reading_books=KarmaBoard.objects.create(
            owner=user,
            name="Czytanie książek",
            unsplash_photo=photos.library,
            sort_index=0.7,
        ),
    )
    return karmaboards
