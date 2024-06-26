# Generated by Django 5.0.6 on 2024-06-16 13:57

from django.conf import settings
from django.db import migrations, models

import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("steps", "0004_questionstep"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAnswerForQuestionStep",
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
                ("answer", models.CharField(verbose_name="Ответ пользователя")),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_answer_for_question_steps",
                        to="steps.questionstep",
                        verbose_name="Вопрос",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="user_answer_for_question_steps",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Шаг [Вопрос][Ответ]",
                "verbose_name_plural": "4. Шаги [Вопрос] -> [Ответ]",
                "db_table": "user_answer_for_question_steps",
                "ordering": ["pk"],
            },
        ),
    ]
