# Generated by Django 5.0.6 on 2024-06-16 14:03

from django.conf import settings
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("steps", "0011_userstepenroll"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Дата обновления")),
                (
                    "title",
                    models.CharField(max_length=255, unique=True, verbose_name="Название курса"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Опубликовать курс"),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True, upload_to="icon/course/", verbose_name="Иконка курса"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание курса")),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "1. Курсы",
                "db_table": "courses",
                "ordering": ["pk"],
            },
        ),
    ]
