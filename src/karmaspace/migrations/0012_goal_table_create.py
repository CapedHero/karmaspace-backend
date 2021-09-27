# Generated by Django 3.2.7 on 2021-09-26 13:43

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("karmaspace", "0011_karmaboard_table_add_field_unsplash_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Goal",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "target_value",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(-99),
                            django.core.validators.MaxValueValidator(99),
                        ]
                    ),
                ),
                (
                    "timeframe",
                    models.CharField(
                        choices=[("DAILY", "Daily"), ("WEEKLY", "Weekly"), ("MONTHLY", "Monthly")],
                        max_length=20,
                    ),
                ),
                (
                    "karmaboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goals",
                        to="karmaspace.karmaboard",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Goal",
                "verbose_name_plural": "Goals",
            },
        ),
    ]