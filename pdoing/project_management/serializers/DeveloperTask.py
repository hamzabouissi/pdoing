from rest_framework import serializers

from pdoing.project_management.models import DeveloperTask, Project


class DeveloperTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperTask
        fields = ("id", "developer", "task", "status", "submit", "created_at")


class DeveloperTaskCreateSerializer(serializers.ModelSerializer):
    assigned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DeveloperTask
        fields = ("id", "developer", "assigned_by", "task", "created_at")


class SubmitDeveloperTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperTask
        fields = ("id", "submit")
