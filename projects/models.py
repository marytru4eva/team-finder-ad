from django.conf import settings
from django.db import models

from projects.constants import (
    PROJECT_NAME_MAX_LENGTH,
    SKILL_NAME_MAX_LENGTH,
    STATUS_CHOICES,
    STATUS_MAX_LENGTH,
    STATUS_OPEN,
)


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
    )
    skills = models.ManyToManyField(
        Skill,
        related_name="projects",
        blank=True,
    )

    def __str__(self):
        return self.name
