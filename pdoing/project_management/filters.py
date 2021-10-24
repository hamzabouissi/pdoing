from django_filters import rest_framework as filters
from pdoing.project_management.models import Task, DeveloperTask


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = ("project",)


class DeveloperTaskFilter(filters.FilterSet):
    class Meta:
        model = DeveloperTask
        fields = ('status',)
