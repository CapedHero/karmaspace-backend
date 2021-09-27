import django


django.setup()

from fixtures.constants import UNSPLASH_PHOTO_1_ID, UNSPLASH_PHOTO_2_ID, UNSPLASH_PHOTO_3_ID
from src.karmaspace.models.unsplash_photo import UnsplashPhoto


UnsplashPhoto.objects.create(
    id=UNSPLASH_PHOTO_1_ID,
    regular_url="https://images.unsplash.com/photo-1631119460950-583cd4801910?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MTV8WF92blp0MmZQend8fHx8fDJ8fDE2MzI3NzgwMzE&ixlib=rb-1.2.1&q=80&w=1080",
    small_url="https://images.unsplash.com/photo-1631119460950-583cd4801910?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MTV8WF92blp0MmZQend8fHx8fDJ8fDE2MzI3NzgwMzE&ixlib=rb-1.2.1&q=80&w=400",
    author_name="Colin Cassidy",
    author_url="https://unsplash.com/@colincassidy",
)

UnsplashPhoto.objects.create(
    id=UNSPLASH_PHOTO_2_ID,
    regular_url="https://images.unsplash.com/photo-1570641963303-92ce4845ed4c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MTh8WF92blp0MmZQend8fHx8fDJ8fDE2MzI3NzgwMzE&ixlib=rb-1.2.1&q=80&w=1080",
    small_url="https://images.unsplash.com/photo-1570641963303-92ce4845ed4c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MTh8WF92blp0MmZQend8fHx8fDJ8fDE2MzI3NzgwMzE&ixlib=rb-1.2.1&q=80&w=400",
    author_name="Massimiliano Morosinotto",
    author_url="https://unsplash.com/@therawhunter",
)

UnsplashPhoto.objects.create(
    id=UNSPLASH_PHOTO_3_ID,
    regular_url="https://images.unsplash.com/photo-1626888637475-e42a70122b59?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258NnxYX3ZuWnQyZlB6d3x8fHx8Mnx8MTYzMjc3ODAzMQ&ixlib=rb-1.2.1&q=80&w=1080",
    small_url="https://images.unsplash.com/photo-1626888637475-e42a70122b59?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258NnxYX3ZuWnQyZlB6d3x8fHx8Mnx8MTYzMjc3ODAzMQ&ixlib=rb-1.2.1&q=80&w=400",
    author_name="Daniel J. Schwarz",
    author_url="https://unsplash.com/@danieljschwarz",
)
