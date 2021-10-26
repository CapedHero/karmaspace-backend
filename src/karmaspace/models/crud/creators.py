from typing import Optional

from django.core.exceptions import ValidationError
from django.db import transaction

from src.app_auth.models import User
from .. import KarmaBoardInvitation, KarmaBoardUser, UnsplashPhoto
from ..karmaboard import KarmaBoard


def create_karmaboard(
    owner: User,
    name: str,
    unsplash_photo: UnsplashPhoto,
    value_step: Optional[KarmaBoard.ValueStep] = None,
    sort_index: Optional[float] = None,
    invitation_secret: Optional[str] = None,
) -> KarmaBoard:
    if KarmaBoardUser.objects.filter(
        karmaboard__name=name,
        user=owner,
        user_role=KarmaBoardUser.UserRole.OWNER,
    ).exists():
        raise ValidationError(f'User {owner.username} already owns KarmaBoard named "{name}".')

    karmaboard = KarmaBoard(
        name=name,
        unsplash_photo=unsplash_photo,
    )
    if value_step:
        karmaboard.value_step = value_step

    karmaboard_user = KarmaBoardUser(
        karmaboard=karmaboard,
        user=owner,
        user_role=KarmaBoardUser.UserRole.OWNER,
    )
    if sort_index:
        karmaboard_user.sort_index = sort_index

    with transaction.atomic():
        karmaboard.save()
        karmaboard_user.save()

        if invitation_secret:
            karmaboard_invitation = KarmaBoardInvitation.objects.get(secret=invitation_secret)
            karmaboard_invitation.karmaboard = karmaboard
            karmaboard_invitation.save()
        else:
            KarmaBoardInvitation.objects.create(karmaboard=karmaboard)

    return karmaboard
