from django_filters import rest_framework as filters
from pdoing.project_management.models import Task


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = ("project",)
