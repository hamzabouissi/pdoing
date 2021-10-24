from typing import Any

from django.db import models


class DeveloperTaskManagerTask(models.Manager):
    def has_all_previous_tasks_solved(self, developer: int, project: int,task_id:int) -> bool:
        from pdoing.project_management.models import DeveloperTaskStatus
            #todo solve this
        tasks = self.filter(
            task__project_id=project,
            developer_id=developer,
        )\
            .exclude(id=task_id)\
            .exclude(status=DeveloperTaskStatus.Successful)
        return not tasks.exists()
