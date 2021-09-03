# Generated by Django 3.2.7 on 2021-09-03 13:46

from django.db import migrations


def populate_sort_index_fields(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    KarmaBoard = apps.get_model("karmaspace", "KarmaBoard")

    karmaboards = KarmaBoard.objects.using(db_alias).order_by("name").all()
    for index, karmaboard in enumerate(karmaboards):
        karmaboard.sort_index = 1.0 / (len(karmaboards) + 1) * (index + 1)
        karmaboard.save()


class Migration(migrations.Migration):

    dependencies = [("karmaspace", "0005_karmaboard_table_add_sort_index_field")]

    operations = [
        migrations.RunPython(
            code=populate_sort_index_fields,
            reverse_code=migrations.RunPython.noop,
        )
    ]
