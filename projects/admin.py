from django.contrib import admin
from .models import Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "project_count")
    search_fields = ("name",)
    list_filter = ("name",)

    @admin.display(description="Количество проектов")
    def project_count(self, obj):
        return obj.projects.count()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status", "participant_count")
    search_fields = ("name", "owner__email")
    list_filter = ("status",)

    @admin.display(description="Количество участников")
    def participant_count(self, obj):
        return obj.participants.count()
