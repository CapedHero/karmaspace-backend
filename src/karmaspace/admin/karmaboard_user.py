from django.contrib import admin

from src.core.utils import get_link_to_admin_form_for_object
from ..models import KarmaBoardUser


@admin.register(KarmaBoardUser)
class KarmaBoardUserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "karmaboard_id",
        "karmaboard_name",
        "user_link",
        "user_role",
        "sort_index",
        "modified_at",
        "created_at",
    ]
    list_display_links = list_display
    ordering = ["-created_at"]
    search_fields = ["karmaboard__id", "karmaboard__name", "user__username"]
    list_filter = ["user__is_demo"]

    fieldsets = [
        [
            "None",
            {
                "fields": [
                    "id",
                    "karmaboard",
                    "user",
                    "user_role",
                    "sort_index",
                ]
            },
        ],
        ["Dates", {"fields": ["modified_at", "created_at"]}],
    ]
    readonly_fields = ["id", "modified_at", "created_at"]

    def karmaboard_id(self, karmaboard_user: KarmaBoardUser) -> str:
        return get_link_to_admin_form_for_object(
            obj=karmaboard_user.karmaboard,
            inner_html=karmaboard_user.karmaboard.id,
        )

    karmaboard_id.short_description = "KarmaBoard ID"

    def karmaboard_name(self, karmaboard_user: KarmaBoardUser) -> str:
        return get_link_to_admin_form_for_object(
            obj=karmaboard_user.karmaboard,
            inner_html=karmaboard_user.karmaboard.name,
        )

    karmaboard_name.short_description = "KarmaBoard Name"

    def user_link(self, karmaboard_user: KarmaBoardUser) -> str:
        return get_link_to_admin_form_for_object(
            obj=karmaboard_user.user,
            inner_html=karmaboard_user.user.username,
        )

    user_link.short_description = "User"
