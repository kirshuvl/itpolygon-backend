from django.urls import path

from core.apps.courses.lms.views import CourseListAPIView, CourseRetrieveAPIView

urlpatterns = [
    path(
        "courses/",
        CourseListAPIView.as_view(),
    ),
    path(
        "courses/<int:courseId>/",
        CourseRetrieveAPIView.as_view(),
    ),
]
