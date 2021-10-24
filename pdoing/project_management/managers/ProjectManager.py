from django.db import models
from django.db.models import QuerySet


class ProjectManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def get_all(self) -> QuerySet:
        return super().get_queryset()

    def is_member_of_project(self, project_id: int, user_id: int) -> bool:
        # DeveloperTask.objects.
        return True
