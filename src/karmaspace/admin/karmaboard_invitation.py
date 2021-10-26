from django.contrib import admin

from src.core.utils import get_link_to_admin_form_for_object
from ..models import KarmaBoardInvitation


@admin.register(KarmaBoardInvitation)
class KarmaBoardInvitationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "karmaboard_id",
        "karmaboard_name",
        "secret",
        "modified_at",
        "created_at",
    ]
    list_display_links = list_display
    ordering = ["-created_at"]
    search_fields = ["karmaboard__id", "karmaboard__name"]

    fieldsets = [
        [
            "None",
            {
                "fields": [
                    "id",
                    "karmaboard",
                    "secret",
                ]
            },
        ],
        ["Dates", {"fields": ["modified_at", "created_at"]}],
    ]
    readonly_fields = ["id", "modified_at", "created_at"]

    def karmaboard_id(self, karmaboard_invitation: KarmaBoardInvitation) -> str:
        if not karmaboard_invitation.karmaboard:
            return ""

        return get_link_to_admin_form_for_object(
            obj=karmaboard_invitation.karmaboard,
            inner_html=karmaboard_invitation.karmaboard.id,
        )

    karmaboard_id.short_description = "KarmaBoard ID"

    def karmaboard_name(self, karmaboard_invitation: KarmaBoardInvitation) -> str:
        if not karmaboard_invitation.karmaboard:
            return ""

        return get_link_to_admin_form_for_object(
            obj=karmaboard_invitation.karmaboard,
            inner_html=karmaboard_invitation.karmaboard.name,
        )

    karmaboard_name.short_description = "KarmaBoard Name"
