from typing import Any

from django.db import models
from django.db.models import QuerySet


class TaskManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def get_all(self) -> QuerySet:
        return super().get_queryset()
