from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.users.models import CustomUser


class StepManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "textstep",
                "videostep",
                "questionstep",
                "problemstep",
                "singlechoicequestionstep",
            )
        )


class DefaultStepManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("step_ptr")


class Step(TimedBaseModel):
    title = models.CharField(
        verbose_name="Название шага",
        max_length=50,
        null=True,
        blank=True,
    )

    is_published = models.BooleanField(
        verbose_name="Опубликовать шаг",
        default=True,
    )

    liked_by = models.BigIntegerField(
        verbose_name="Счетчик лайков",
        default=0,
    )

    bookmarked_by = models.BigIntegerField(
        verbose_name="Счетчик закладок",
        default=0,
    )

    viewed_by = models.BigIntegerField(
        verbose_name="Счетчик просмотров",
        default=0,
    )

    objects = StepManager()

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "1. Шаги"
        ordering = ["pk"]
        db_table = "steps"

    def get_type(self):
        if hasattr(self, "textstep"):
            return "textstep"
        elif hasattr(self, "videostep"):
            return "videostep"
        elif hasattr(self, "questionstep"):
            return "questionstep"
        elif hasattr(self, "problemstep"):
            return "problemstep"
        elif hasattr(self, "singlechoicequestionstep"):
            return "singlechoicequestionstep"
        return None

    def __str__(self):
        data = {
            "textstep": "[Шаг][Текст]",
            "videostep": "[Шаг][Видео]",
            "questionstep": "[Шаг][Вопрос]",
            "problemstep": "[Шаг][Задача]",
            "singlechoicequestionstep": "[Шаг][Вопрос с выбором ответа]",
            None: "[Шаг][None]",
        }
        return f"{data[self.get_type()]} № {self.pk}"


class TextStep(Step):
    text = models.JSONField(
        verbose_name="Текст",
    )

    objects = DefaultStepManager()

    class Meta:
        verbose_name = "Шаг [Текстовый]"
        verbose_name_plural = "2. Шаги [Текстовые]"
        ordering = ["pk"]
        db_table = "steps_textsteps"


class VideoStep(Step):
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        max_length=500,
    )

    objects = DefaultStepManager()

    class Meta:
        verbose_name = "Шаг [Видео]"
        verbose_name_plural = "3. Шаги [Видео]"
        ordering = ["pk"]
        db_table = "steps_videosteps"


class QuestionStep(Step):
    text = models.JSONField(
        verbose_name="Текст вопроса",
    )

    answer = models.CharField(
        verbose_name="Ответ на вопрос",
    )

    objects = DefaultStepManager()

    class Meta:
        verbose_name = "Шаг [Вопрос]"
        verbose_name_plural = "4. Шаги [Вопрос]"
        ordering = ["pk"]
        db_table = "steps_questionsteps"


class UserAnswerForQuestionStep(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_answer_for_question_steps",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
    )

    question = models.ForeignKey(
        QuestionStep,
        related_name="user_answer_for_question_steps",
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
    )

    answer = models.CharField(
        verbose_name="Ответ пользователя",
    )

    is_correct = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = "Шаг [Вопрос][Ответ]"
        verbose_name_plural = "4. Шаги [Вопрос] -> [Ответ]"
        ordering = ["pk"]
        db_table = "user_answer_for_question_steps"


class SingleChoiceQuestionStep(Step):
    text = models.JSONField(
        verbose_name="Текст вопроса",
    )

    objects = DefaultStepManager()

    class Meta:
        verbose_name = "Шаг [Вопрос][Выбор ответа]"
        verbose_name_plural = "4. Шаги [Вопрос][Выбор ответа]"
        ordering = ["pk"]
        db_table = "steps_singlechoicesteps"


class AnswerForSingleChoiceQuestionStep(TimedBaseModel):
    answer = models.CharField(
        verbose_name="Ответ",
    )

    question = models.ForeignKey(
        SingleChoiceQuestionStep,
        related_name="answer_for_single_choice_question_steps",
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
    )

    is_correct = models.BooleanField(
        verbose_name="Верный ответ",
        default=False,
    )

    class Meta:
        verbose_name = "Шаг [Вопрос][Выбор ответа] -> [Варианты ответа]"
        verbose_name_plural = "4. Шаги [Вопрос][Выбор ответа] -> [Варианты ответов]"
        ordering = ["pk"]
        db_table = "answer_for_single_choice_question_steps"


class UserAnswerForSingleChoiceQuestionStep(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_answer_for_single_choice_question_steps",
        verbose_name="Студент",
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        SingleChoiceQuestionStep,
        related_name="user_answer_for_single_choice_question_steps",
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
    )

    answer = models.ForeignKey(
        AnswerForSingleChoiceQuestionStep,
        related_name="user_answer_for_single_choice_question_steps",
        verbose_name="Ответ",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Шаг [Вопрос][Выбор ответа] -> [Ответ]"
        verbose_name_plural = "4. Шаги [Вопрос][Выбор ответа] -> [Ответы]"
        ordering = ["pk"]
        db_table = "user_answer_for_single_choice_question_steps"


class ProblemStep(Step):
    text = models.JSONField(
        verbose_name="Легенда задачи",
    )

    input = models.JSONField(
        verbose_name="Входные данные",
    )

    output = models.JSONField(
        verbose_name="Выходные данные",
    )

    notes = models.JSONField(
        verbose_name="Примечания",
    )

    start_code = models.TextField(
        verbose_name="Дополнительный код",
        max_length=10000,
        blank=True,
        default="",
    )

    first_sample = models.IntegerField(
        verbose_name="Номер первого сэмпла",
        default=1,
    )

    last_sample = models.IntegerField(
        verbose_name="Номер последнего сэмпла",
        default=3,
    )

    first_test = models.IntegerField(
        verbose_name="Номер первого теста",
        default=1,
    )

    cpu_time = models.IntegerField(
        verbose_name="Ограничение по времени",
        default=1,
    )

    memory = models.IntegerField(
        verbose_name="Ограничение по памяти",
        default=64,
    )

    objects = DefaultStepManager()

    class Meta:
        verbose_name = "Шаг [Программирование]"
        verbose_name_plural = "5. Шаги [Программирование]"
        ordering = ["pk"]
        db_table = "steps_problemsteps"


class TestForProblemStep(TimedBaseModel):
    problem = models.ForeignKey(
        ProblemStep,
        related_name="tests",
        verbose_name="Задача",
        on_delete=models.CASCADE,
    )

    number = models.IntegerField(
        verbose_name="№ теста",
        default=1000,
    )

    input = models.TextField(
        verbose_name="Входные данные",
        max_length=100000,
        blank=True,
    )

    output = models.TextField(
        verbose_name="Выходные данные",
        max_length=100000,
        blank=True,
    )

    class Meta:
        verbose_name = "Шаг [Программирование][Тест]"
        verbose_name_plural = "5. Шаги [Программирование][Тесты]"
        ordering = ["pk"]
        unique_together = ("problem", "number")
        db_table = "test_for_problem_steps"


class UserAnswerForProblemStep(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_answer_for_problem_steps",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    code = models.TextField(
        verbose_name="Код пользователя",
        max_length=10000,
    )

    problem = models.ForeignKey(
        ProblemStep,
        related_name="user_answer_for_problem_steps",
        verbose_name="Задача",
        on_delete=models.CASCADE,
    )

    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("cpp", "C++"),
    ]

    language = models.CharField(
        verbose_name="Язык программирования",
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default="python",
    )

    VERDICT_CHOICES = [
        ("PR", "На проверке"),
        ("OK", "OK"),
        ("CE", "Ошибка компиляции"),
        ("WA", "Неправильный ответ"),
        ("TL", "Превышение времени"),
        ("ML", "Превышение памяти"),
        ("UN", "Незвестная ошибка"),
    ]

    verdict = models.CharField(
        verbose_name="Вердикт",
        max_length=2,
        choices=VERDICT_CHOICES,
        default="PR",
    )

    cpu_time = models.FloatField(
        verbose_name="Затраченное время",
        null=True,
    )

    first_fail_test = models.IntegerField(
        verbose_name="Первый ошибочный тест",
        null=True,
    )

    points = models.IntegerField(
        verbose_name="Баллы",
        null=True,
    )

    class Meta:
        verbose_name = "Попытка пользователя"
        verbose_name_plural = "5. Шаги [Программирование] -> [Ответ]"
        ordering = ["pk"]


class UserAnswerForTestForProblemStep(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_answer_for_test_for_problem_steps",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    code = models.ForeignKey(
        UserAnswerForProblemStep,
        related_name="user_answer_for_test_for_problem_steps",
        verbose_name="Решение пользователя",
        on_delete=models.CASCADE,
    )

    test = models.ForeignKey(
        TestForProblemStep,
        related_name="user_answer_for_test_for_problem_steps",
        verbose_name="Тест",
        on_delete=models.CASCADE,
    )

    VERDICT_CHOICES = [
        ("PR", "На проверке"),
        ("OK", "OK"),
        ("CE", "Ошибка компиляции"),
        ("WA", "Неправильный ответ"),
        ("TL", "Превышение времени"),
        ("ML", "Превышение памяти"),
        ("UN", "Незвестная ошибка"),
    ]

    verdict = models.CharField(
        verbose_name="Вердикт",
        max_length=2,
        choices=VERDICT_CHOICES,
        default="WA",
    )

    exit_code = models.IntegerField(
        verbose_name="exit_code",
    )

    stdout = models.TextField(
        verbose_name="stdout",
        max_length=10000,
    )

    stderr = models.TextField(
        verbose_name="stderr",
        max_length=10000,
    )

    duration = models.FloatField(
        verbose_name="duration",
        default=0,
    )

    timeout = models.BooleanField(
        verbose_name="timeout",
        default=False,
    )

    oom_killed = models.BooleanField(
        verbose_name="oom_killed",
        default=False,
    )

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "5. Шаги [Программирование][Тесты] -> [Ответ]"
        ordering = ["pk"]


class UserStepEnroll(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_step_enrolls",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    step = models.ForeignKey(
        Step,
        related_name="user_step_enrolls",
        verbose_name="Шаг",
        on_delete=models.CASCADE,
    )

    STATUS_CHOICES = [
        ("PR", "Шаг изучается"),
        ("RP", "Шаг повторяется"),
        ("WA", "Шаг не сдан"),
        ("OK", "Шаг пройден"),
        ("WT", "Шаг на проверке"),
    ]

    status = models.CharField(
        verbose_name="Статус",
        max_length=2,
        choices=STATUS_CHOICES,
        default="PR",
    )

    class Meta:
        verbose_name = "Шаг -> Пользователь [Сайт]"
        verbose_name_plural = "6. Шаги -> Пользователи [Сайт]"
        ordering = ["pk"]
        unique_together = (
            "step",
            "user",
        )
        db_table = "user_step_enrolls"


class UserStepLike(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_step_likes",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    step = models.ForeignKey(
        Step,
        related_name="user_step_likes",
        verbose_name="Шаг",
        on_delete=models.CASCADE,
    )

    SOURCE_CHOICES = [
        ("LMS", "LMS"),
        ("BOT", "Телеграм Бот"),
    ]

    source = models.CharField(
        verbose_name="Источник",
        max_length=3,
        choices=SOURCE_CHOICES,
        default="LMS",
    )

    class Meta:
        verbose_name = "Шаг -> Лайк [Сайт]"
        verbose_name_plural = "7. Шаги -> Лайки [Сайт]"
        ordering = ["pk"]
        unique_together = (
            "step",
            "user",
        )
        db_table = "user_step_likes"


class UserStepBookmark(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_step_bookmarks",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    step = models.ForeignKey(
        Step,
        related_name="user_step_bookmarks",
        verbose_name="Шаг",
        on_delete=models.CASCADE,
    )

    SOURCE_CHOICES = [
        ("LMS", "LMS"),
        ("BOT", "Телеграм Бот"),
    ]

    source = models.CharField(
        verbose_name="Источник",
        max_length=3,
        choices=SOURCE_CHOICES,
        default="LMS",
    )

    class Meta:
        verbose_name = "Шаг -> Закладка [Сайт]"
        verbose_name_plural = "8. Шаги -> Закладки [Сайт]"
        ordering = ["pk"]
        unique_together = (
            "step",
            "user",
        )
        db_table = "user_step_bookmarks"


class UserStepView(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        related_name="user_step_views",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    step = models.ForeignKey(
        Step,
        related_name="user_step_views",
        verbose_name="Шаг",
        on_delete=models.CASCADE,
    )

    SOURCE_CHOICES = [
        ("LMS", "LMS"),
        ("BOT", "Телеграм Бот"),
    ]

    source = models.CharField(
        verbose_name="Источник",
        max_length=3,
        choices=SOURCE_CHOICES,
        default="LMS",
    )

    class Meta:
        verbose_name = "Шаг -> Просмотр [Сайт]"
        verbose_name_plural = "9. Шаги -> Просмотры [Сайт]"
        ordering = ["pk"]
        db_table = "user_step_views"
