from rest_framework import serializers

from pdoing.project_management.models import Task

# class TaskProjectSerializer


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "project", "description", "duration", "created_at")


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "project", "description", "duration", "public", "created_at")

    def validate(self, attrs):
        super().validate(attrs)
        request = self.context.get("request")
        project = attrs.get("project")
        if project.author != request.user:
            raise serializers.ValidationError(
                {"project": "You're not the project's author"}
            )
        return attrs


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "duration", "public")

    def validate(self, attrs):
        super().validate(attrs)
        request = self.context.get("request")
        project = attrs.get("project")
        if project.author != request.user:
            raise serializers.ValidationError(
                {"project": "You're not the project's author"}
            )
        return attrs
