from django.contrib import admin

from pdoing.project_management.models import DeveloperTask, Project, Task

# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(DeveloperTask)
