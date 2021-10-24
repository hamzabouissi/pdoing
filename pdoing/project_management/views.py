from django.shortcuts import render
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from pdoing.core.Base import SerilizerNone
from pdoing.project_management.filters import TaskFilter, DeveloperTaskFilter
from pdoing.project_management.models import DeveloperTask, Project, Task
from pdoing.project_management.permissions import (
    DeveloperTaskOwnerPermission,
    IsInstructorPermission,
    TaskCreatorPermission,
)
from pdoing.project_management.serializers.DeveloperTask import (
    DeveloperTaskCreateSerializer,
    DeveloperTaskListSerializer,
    SubmitDeveloperTaskSerializer,
)
from pdoing.project_management.serializers.Project import (
    ProjectAddSerializer,
    ProjectListSerializer,
)
from pdoing.project_management.serializers.Task import (
    TaskCreateSerializer,
    TaskListSerializer, TaskUpdateSerializer,
)

# Create your views here.
from pdoing.users.models import UserTypeEnum


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializers = {
        "list": ProjectListSerializer,
        "create": ProjectAddSerializer,
        "retrieve": ProjectListSerializer,
    }
    permission_classes = (IsInstructorPermission,)

    def get_serializer_class(self):
        return self.serializers.get(self.action, SerilizerNone)


class TaskView(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "patch")
    queryset = Task.objects.all()
    serializers = {
        "list": TaskListSerializer,
        "create": TaskCreateSerializer,
        "update": TaskUpdateSerializer
    }
    permission_classes = (IsInstructorPermission,)
    filterset_class = TaskFilter

    def get_serializer_class(self):
        return self.serializers.get(self.action, SerilizerNone)


class DeveloperTaskView(viewsets.ModelViewSet):
    http_method_names = ("get", "post")
    queryset = DeveloperTask.objects.all()
    serializers = {
        "list": DeveloperTaskListSerializer,
        "create": DeveloperTaskCreateSerializer,
        "retrieve": DeveloperTaskListSerializer,
        "submit": SubmitDeveloperTaskSerializer,
    }
    filterset_class = DeveloperTaskFilter

    def get_serializer_class(self):
        return self.serializers.get(self.action, SerilizerNone)

    def create(self, request, *args, **kwargs):
        if request.user.user_type != UserTypeEnum.Instructor:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            TaskCreatorPermission,
        ],
    )
    def accept(self, request, pk=None):
        developer_task: DeveloperTask = self.get_object()
        developer_task.accept()
        developer_task.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            TaskCreatorPermission,
        ],
    )
    def cancel(self, request, pk=None):
        developer_task: DeveloperTask = self.get_object()
        developer_task.cancel()
        developer_task.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            DeveloperTaskOwnerPermission,
        ],
    )
    def submit(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        developer_task: DeveloperTask = self.get_object()
        result = developer_task.submit_answer(data["submit"])
        if result.is_failure:
            return Response(result.error_message, status.HTTP_400_BAD_REQUEST)
        developer_task.save()
        return Response(status=status.HTTP_202_ACCEPTED)
