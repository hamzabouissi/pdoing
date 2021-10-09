from django.apps import AppConfig


class ProjectManagementConfig(AppConfig):
    name = "pdoing.project_management"

    def ready(self):
        try:
            import pdoing.users.signals  # noqa F401
        except ImportError:
            pass
