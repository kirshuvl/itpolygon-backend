# Generated by Django 5.0.6 on 2024-07-28 13:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("steps", "0017_answerforsinglechoicequestionstep"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAnswerForSingleChoiceQuestionStep",
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
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_answer_for_single_choice_question_steps",
                        to="steps.answerforsinglechoicequestionstep",
                        verbose_name="Ответ",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_answer_for_single_choice_question_steps",
                        to="steps.singlechoicequestionstep",
                        verbose_name="Вопрос",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_answer_for_single_choice_question_steps",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Студент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Шаг [Вопрос][Выбор ответа] -> [Ответ]",
                "verbose_name_plural": "4. Шаги [Вопрос][Выбор ответа] -> [Ответы]",
                "db_table": "user_answer_for_single_choice_question_steps",
                "ordering": ["pk"],
            },
        ),
    ]
