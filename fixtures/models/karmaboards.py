from dataclasses import dataclass

from fixtures.models.unsplash_photos import Photos
from src.app_auth.models import User
from src.karmaspace.models import KarmaBoard
from src.karmaspace.models.crud.creators import create_karmaboard


@dataclass
class KarmaBoards:
    duties_and_leasure: KarmaBoard
    family_relations: KarmaBoard
    fitness_and_health: KarmaBoard
    house_chores: KarmaBoard
    learning_english: KarmaBoard
    learning_guitar: KarmaBoard
    personal_growth: KarmaBoard
    plants: KarmaBoard
    reading_books: KarmaBoard


def create_karmaboards(user: User, photos: Photos) -> KarmaBoards:
    karmaboards = KarmaBoards(
        duties_and_leasure=create_karmaboard(
            owner=user,
            name="Obowiązki i rozrywki Hani",
            unsplash_photo=photos.sunflowers,
            sort_index=0.1,
        ),
        family_relations=create_karmaboard(
            owner=user,
            name="Relacje rodzinne",
            unsplash_photo=photos.family,
            sort_index=0.8,
        ),
        fitness_and_health=create_karmaboard(
            owner=user,
            name="Sport i zdrowie",
            unsplash_photo=photos.bowl_food,
            sort_index=0.3,
        ),
        house_chores=create_karmaboard(
            owner=user,
            name="Dom i porządki",
            unsplash_photo=photos.wooden_house,
            sort_index=0.2,
        ),
        learning_english=create_karmaboard(
            owner=user,
            name="Nauka angielskiego",
            unsplash_photo=photos.english_flag,
            sort_index=0.5,
        ),
        learning_guitar=create_karmaboard(
            owner=user,
            name="Gitara",
            unsplash_photo=photos.guitar,
            sort_index=0.6,
        ),
        personal_growth=create_karmaboard(
            owner=user,
            name="Rozwój w wolnym czasie",
            unsplash_photo=photos.balloons_over_plain,
            sort_index=0.05,
        ),
        plants=create_karmaboard(
            owner=user,
            name="Rośliny",
            unsplash_photo=photos.succulents,
            sort_index=0.4,
        ),
        reading_books=create_karmaboard(
            owner=user,
            name="Czytanie książek",
            unsplash_photo=photos.library,
            sort_index=0.7,
        ),
    )
    return karmaboards
