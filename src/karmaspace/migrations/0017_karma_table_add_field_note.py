# Generated by Django 3.2.8 on 2021-10-15 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("karmaspace", "0016_karma_table_add_task_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="karma",
            name="note",
            field=models.TextField(blank=True, default="", max_length=1000),
        ),
    ]