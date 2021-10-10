from django.contrib import admin

from src.core.utils import get_link_to_admin_form_for_object
from ..models import Karma


@admin.register(Karma)
class KarmaAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "karmaboard_owner_link",
        "karmaboard_link",
        "name",
        "value",
        "duration_in_m",
        "modified_at",
        "created_at",
    ]
    list_display_links = list_display
    ordering = ["-created_at"]
    search_fields = ["id", "name", "karmaboard__name", "karmaboard__owner__username"]
    date_hierarchy = "modified_at"

    fieldsets = [
        [
            "None",
            {
                "fields": [
                    "id",
                    "karmaboard",
                    "name",
                    "value",
                    "duration_in_m",
                ]
            },
        ],
        ["Dates", {"fields": ["modified_at", "created_at"]}],
    ]
    readonly_fields = ["id", "modified_at", "created_at"]

    def karmaboard_owner_link(self, karma: Karma) -> str:
        return get_link_to_admin_form_for_object(
            obj=karma.karmaboard.owner,
            inner_html=karma.karmaboard.owner.username,
        )

    karmaboard_owner_link.short_description = "KarmaBoard Owner"
    karmaboard_owner_link.admin_order_field = "karmaboard__owner__username"

    def karmaboard_link(self, karma: Karma) -> str:
        return get_link_to_admin_form_for_object(
            obj=karma.karmaboard,
            inner_html=karma.karmaboard.name,
        )

    karmaboard_link.short_description = "KarmaBoard"
    karmaboard_link.admin_order_field = "karmaboard__name"
