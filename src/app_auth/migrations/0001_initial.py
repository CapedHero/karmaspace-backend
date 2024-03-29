# Generated by Django 3.1.7 on 2021-04-24 13:18
from uuid import uuid4

import django.contrib.auth.models
import django.contrib.postgres.fields.citext
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations, models

import src.app_auth.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        CITextExtension(),
        migrations.CreateModel(
            name="PassphraseRecord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("passphrase", models.CharField(max_length=50)),
                ("expires_at", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Passphrase Record",
                "verbose_name_plural": "Passphrase Records",
            },
        ),
        migrations.CreateModel(
            name="ProxyGroup",
            fields=[],
            options={
                "verbose_name": "group",
                "verbose_name_plural": "groups",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.group",),
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "username",
                    django.contrib.postgres.fields.citext.CICharField(
                        max_length=50,
                        unique=True,
                        validators=[src.app_auth.models.user.UsernameValidator()],
                    ),
                ),
                ("full_name", models.CharField(blank=True, default="", max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=src.app_auth.models.user.get_avatar_upload_to_path,
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                    ),
                ),
                ("password", models.CharField(blank=True, max_length=128)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
