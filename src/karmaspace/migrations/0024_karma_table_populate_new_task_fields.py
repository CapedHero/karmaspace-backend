# Generated by Django 3.2.7 on 2021-10-24 21:41

from django.db import migrations


def populate_karmaboard_invitation_table(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Karma = apps.get_model("karmaspace", "Karma")

    for karma in Karma.objects.using(db_alias).all():
        if karma.is_task:
            karma.is_active_task = not bool(karma.completed_at)
        else:
            karma.completed_at = karma.created_at
        karma.save()


class Migration(migrations.Migration):

    dependencies = [("karmaspace", "0023_karma_table_add_field_is_active_task")]

    operations = [
        migrations.RunPython(
            code=populate_karmaboard_invitation_table,
            reverse_code=migrations.RunPython.noop,
        )
    ]
