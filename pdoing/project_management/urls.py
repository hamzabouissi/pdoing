from django.urls import path
from rest_framework.routers import DefaultRouter
from pdoing.project_management.views import DeveloperTaskView, ProjectView, TaskView

app_name = "project_management"
router = DefaultRouter()
router.register(r"projects", ProjectView, basename="project")
router.register(r"tasks", TaskView, basename="task")
router.register(r"developerTask", DeveloperTaskView, basename="task")


urlpatterns = [
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
urlpatterns += router.urls
