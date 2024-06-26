# Generated by Django 5.0.6 on 2024-06-16 13:59

from django.conf import settings
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("steps", "0006_problemstep"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TestForProblemStep",
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
                ("number", models.IntegerField(default=1000, verbose_name="№ теста")),
                (
                    "input",
                    models.TextField(blank=True, max_length=100000, verbose_name="Входные данные"),
                ),
                (
                    "output",
                    models.TextField(blank=True, max_length=100000, verbose_name="Выходные данные"),
                ),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tests",
                        to="steps.problemstep",
                        verbose_name="Задача",
                    ),
                ),
            ],
            options={
                "verbose_name": "Шаг [Программирование][Тест]",
                "verbose_name_plural": "5. Шаги [Программирование][Тесты]",
                "db_table": "test_for_problem_steps",
                "ordering": ["pk"],
                "unique_together": {("problem", "number")},
            },
        ),
    ]
