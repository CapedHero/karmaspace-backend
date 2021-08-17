from django.contrib import admin
from django.contrib.auth.models import Group


# Unregister default `GroupAdmin` so that we can use the below version.
admin.site.unregister(Group)


class ProxyGroup(Group):
    """
    Proxy model to show `auth.Group` model in Admin Site under "App Auth" group.

    All other methods wreak absolute havoc as they brutally interfere with
    with database and migrations!
    """

    class Meta:
        proxy = True

        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural


@admin.register(ProxyGroup)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("permissions",)
