from typing import Any

from django.db import models


class DeveloperTaskManagerTask(models.Manager):
    def has_all_previous_tasks_solved(self, developer: int, project: int) -> bool:
        from pdoing.project_management.models import DeveloperTaskStatus

        tasks = self.filter(
            task__project_id=project,
            developer_id=developer,
            status__nq=DeveloperTaskStatus.Successful,
        )
        return not tasks.exists()
