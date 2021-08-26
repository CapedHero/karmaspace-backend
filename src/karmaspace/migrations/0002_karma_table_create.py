# Generated by Django 3.1.13 on 2021-08-25 20:02

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("karmaspace", "0001_karmaboard_table_create"),
    ]

    operations = [
        migrations.CreateModel(
            name="Karma",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                (
                    "value",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(-99),
                            django.core.validators.MaxValueValidator(99),
                        ]
                    ),
                ),
                (
                    "karmaboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="karmas",
                        to="karmaspace.karmaboard",
                    ),
                ),
            ],
            options={
                "verbose_name": "Karma",
                "verbose_name_plural": "Karmas",
            },
        ),
    ]