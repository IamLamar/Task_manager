from django.contrib import admin
from task.models import Project,Task,Comment, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('table', 'user', 'data', 'date')



admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)

