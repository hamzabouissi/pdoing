# Create your models here.


from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from pdoing.core.Base import BaseModel, Result
from pdoing.project_management.managers.DeveloperTaskManager import (
    DeveloperTaskManagerTask,
)
from pdoing.project_management.managers.ProjectManager import ProjectManager
from pdoing.project_management.managers.TaskManager import TaskManager
from pdoing.users.models import User, UserTypeEnum


class DeveloperTaskStatus(models.TextChoices):
    Pending = "Pending", _("Pending")
    Submited = "Submited", _("Submited")
    Successful = "Successful", _("Pending")
    Failed = "Failed", _("Failed")


class ProjectDifficulty(models.TextChoices):
    Easy = "Easy", _("Easy")
    Medium = "Medium", _("Medium")
    Hard = "Hard", _("Hard")
    Very_Hard = "Very_Hard", _("Very_Hard")


class Project(BaseModel):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        limit_choices_to={"user_type": UserTypeEnum.Instructor},
    )
    solution = models.CharField(default="", max_length=20)
    duration = models.DurationField(default=timedelta(days=1))
    public = models.BooleanField(default=False)

    objects = ProjectManager()

    def __str__(self) -> str:
        return self.title


class Task(BaseModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=35, default="")
    description = models.TextField(max_length=250)
    duration = models.DurationField(default=timedelta(days=1))
    solution = models.CharField(default="", null=False, blank=False, max_length=20)

    public = models.BooleanField(default=False)

    objects = TaskManager()

    @property
    def author(self):
        return self.project.author


class Hints(BaseModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, blank=False, related_name="hints"
    )
    required_points = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=False)


class DeveloperTask(BaseModel):
    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        related_name="tasks",
        limit_choices_to={"user_type": UserTypeEnum.Instructor},
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": UserTypeEnum.Instructor},
        blank=False,
        related_name="assigned_tasks",
        null=False,
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=False)
    status = models.CharField(
        max_length=20,
        choices=DeveloperTaskStatus.choices,
        default=DeveloperTaskStatus.Pending,
    )
    submit = models.TextField(max_length=40, blank=True, null=True, default="")

    objects = DeveloperTaskManagerTask()

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super(DeveloperTask, self).save(*args, **kwargs)

    def clean(self) -> None:
        self.__is_valid_author()

    def __is_valid_author(self):
        if self.assigned_by != self.task.author:
            raise ValidationError({"assigned_by": "Not Valid project author"})

    def submit_answer(self, submit: str) -> Result:
        # check previous tasks where successful
        if self.objects.has_all_previous_tasks_solved(
            self.developer_id, self.task.project_id
        ):
            self.submit = submit
            self.status = DeveloperTaskStatus.Submited
            return Result.success()
        return Result.failure("previous task weren't completed")

    def accept(self):
        self.status = DeveloperTaskStatus.Successful

    def cancel(self):
        self.status = DeveloperTaskStatus.Failed

    def reached_deadline(self):
        today = datetime.now()
        if (
            self.status == DeveloperTaskStatus.Pending
            and today - self.created_at > self.task.duration
        ):
            return True
        return False
