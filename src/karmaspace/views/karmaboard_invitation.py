from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from ..models import KarmaBoardInvitation, KarmaBoardUser


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def karmaboard_invitations_view(request: Request) -> Response:
    karmaboard_invitation = KarmaBoardInvitation.objects.create()
    return Response(data={"secret": karmaboard_invitation.secret})


class FinishInputSerializer(serializers.Serializer):
    invitation_secret = serializers.CharField(max_length=50)


@api_view(http_method_names=["PUT"])
@permission_classes([IsAuthenticated])
def karmaboard_invitation_finish_view(request: Request) -> Response:
    input_ = FinishInputSerializer(data=request.data)
    input_.is_valid(raise_exception=True)

    karmaboard = KarmaBoardInvitation.objects.get(
        secret=input_.validated_data["invitation_secret"],
    ).karmaboard

    if not karmaboard:
        return Response(data={}, status=HTTP_404_NOT_FOUND)

    try:
        KarmaBoardUser.objects.create(
            karmaboard=karmaboard,
            user=request.user,
            user_role=KarmaBoardUser.UserRole.MEMBER,
        )
        return Response(data={"id": str(karmaboard.id), "is_added": True}, status=HTTP_200_OK)
    except ValidationError:
        return Response(data={"id": str(karmaboard.id), "is_added": False}, status=HTTP_200_OK)
