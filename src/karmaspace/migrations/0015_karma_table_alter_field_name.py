# Generated by Django 3.2.7 on 2021-10-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("karmaspace", "0014_notification_table_delete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="karma",
            name="name",
            field=models.CharField(max_length=75),
        ),
    ]
