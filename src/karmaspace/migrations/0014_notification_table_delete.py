# Generated by Django 3.2.7 on 2021-09-27 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("karmaspace", "0013_notification_table_create"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Notification",
        ),
    ]