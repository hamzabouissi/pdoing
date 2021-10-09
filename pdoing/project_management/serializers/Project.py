from django.contrib.auth import get_user_model
from rest_framework import serializers

from pdoing.project_management.models import Project

User = get_user_model()


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "user_type")


class ProjectListSerializer(serializers.ModelSerializer):
    author = ProjectUserSerializer()

    class Meta:
        model = Project
        fields = ("id", "title", "description", "author", "duration", "created_at")


class ProjectAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "description", "author")
