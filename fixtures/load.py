import django  # isort:skip

django.setup()

from django.conf import settings

from fixtures import models


models.create_admin()

user = models.create_user(
    username=settings.FIXTURES_USER_1_USERNAME,
    email=settings.FIXTURES_USER_1_EMAIL,
)

unsplash_photo_1, unsplash_photo_2, unsplash_photo_3 = models.create_unsplash_photos()

karmaboard_1, karmaboard_2, karmaboard_3 = models.create_karmaboards(
    user,
    unsplash_photo_1,
    unsplash_photo_2,
    unsplash_photo_3,
)

models.create_karmas(karmaboard_1, karmaboard_2, karmaboard_3)

models.create_goals(karmaboard_1)
