# Generated by Django 3.2.8 on 2021-10-26 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("karmaspace", "0024_karma_table_populate_new_task_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="karma",
            name="is_task",
        ),
    ]