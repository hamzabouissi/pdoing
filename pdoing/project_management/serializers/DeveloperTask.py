from datetime import datetime

from rest_framework import serializers

from pdoing.project_management.models import DeveloperTask, Project, Task


class NestedDeveloperTaskSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "duration")


class DeveloperTaskListSerializer(serializers.ModelSerializer):
    task = NestedDeveloperTaskSerialiazer()

    class Meta:
        model = DeveloperTask
        fields = ("id", "developer", "task", "status", "submit", "created_at", "end_date")


class DeveloperTaskCreateSerializer(serializers.ModelSerializer):
    assigned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DeveloperTask
        fields = ("id", "developer", "assigned_by", "task", "created_at")


class SubmitDeveloperTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperTask
        fields = ("id", "submit")
