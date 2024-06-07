from django.contrib import admin

from core.apps.homeworks.models import Homework, HomeworkStepConnection


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "seminar",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "author",
        "seminar",
    )
    search_fields = (
        "id",
        "author",
        "seminar",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "author",
        "seminar",
    )
    ordering = ("id",)


@admin.register(HomeworkStepConnection)
class HomeworkStepConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "homework",
        "step",
        "is_published",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "homework",
        "step",
    )
    search_fields = (
        "id",
        "homework",
        "step",
        "is_published",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "homework",
        "step",
        "is_published",
    )
    ordering = ("id",)