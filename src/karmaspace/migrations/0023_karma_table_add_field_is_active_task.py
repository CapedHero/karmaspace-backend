# Generated by Django 3.2.8 on 2021-10-26 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("karmaspace", "0022_karmaboard_invitation_table_populate"),
    ]

    operations = [
        migrations.AddField(
            model_name="karma",
            name="is_active_task",
            field=models.BooleanField(default=None, null=True, blank=True),
        ),
    ]