from django.contrib import admin

from project.models import ProjectType, Project

admin.site.register(ProjectType)
admin.site.register(Project)