from django.contrib import admin

from src.core.utils import get_link_to_admin_form_for_object
from ..models import KarmaBoard


@admin.register(KarmaBoard)
class KarmaBoardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "owner_link",
        "name",
        "value_step",
        "unsplash_photo_link",
        "sort_index",
        "modified_at",
        "created_at",
    ]
    list_display_links = list_display
    ordering = ["-created_at"]
    search_fields = ["id", "name", "owner__username"]
    date_hierarchy = "modified_at"

    fieldsets = [
        [
            "None",
            {
                "fields": [
                    "id",
                    "owner",
                    "name",
                    "value_step",
                    "unsplash_photo",
                    "sort_index",
                ]
            },
        ],
        ["Dates", {"fields": ["modified_at", "created_at"]}],
    ]
    readonly_fields = ["id", "modified_at", "created_at"]

    def owner_link(self, karmaboard: KarmaBoard) -> str:
        return get_link_to_admin_form_for_object(
            obj=karmaboard.owner,
            inner_html=karmaboard.owner.username,
        )

    owner_link.short_description = "Owner"

    def unsplash_photo_link(self, karmaboard: KarmaBoard) -> str:
        return get_link_to_admin_form_for_object(
            obj=karmaboard.unsplash_photo,
            inner_html=karmaboard.unsplash_photo.id,
        )

    unsplash_photo_link.short_description = "Unsplash Photo"
    unsplash_photo_link.admin_order_field = "unsplash_photo__id"
