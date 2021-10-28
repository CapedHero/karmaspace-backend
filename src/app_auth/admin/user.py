from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ..models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        "id",
        "username",
        "full_name",
        "email",
        "is_active",
        "is_staff",
        "is_demo",
        "is_superuser",
        "groups_list",
        "created_at",
        "modified_at",
    ]
    list_display_links = list_display
    list_filter = ["is_active", "is_demo", "is_staff", "is_superuser"]
    search_fields = ["username", "full_name", "email"]

    fieldsets = [
        [None, {"fields": ["id", "username", "password", "avatar"]}],
        ["Personal info", {"fields": ["full_name", "email"]}],
        [
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_demo",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ],
        ["Dates", {"fields": ["created_at", "modified_at"]}],
    ]
    readonly_fields = ["id", "created_at", "modified_at"]

    add_fieldsets = [
        [None, {"classes": ["wide"], "fields": ["username", "email", "password1", "password2"]}]
    ]

    def groups_list(self, user):
        return list(user.groups.values_list("name", flat=True))

    groups_list.short_description = "Groups"
