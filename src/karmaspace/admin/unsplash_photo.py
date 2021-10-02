from django.contrib import admin

from ..models import UnsplashPhoto


@admin.register(UnsplashPhoto)
class UnsplashPhotoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "regular_url",
        "small_url",
        "author_name",
        "author_url",
    ]
    list_display_links = list_display
    ordering = ["id"]
    search_fields = ["id", "author_name"]

    fieldsets = [
        [
            "None",
            {
                "fields": [
                    "id",
                    "regular_url",
                    "small_url",
                    "author_name",
                    "author_url",
                ]
            },
        ],
        ["Dates", {"fields": ["modified_at", "created_at"]}],
    ]
    readonly_fields = ["id", "modified_at", "created_at"]
