from django.urls import path
from .views import (
    project_list,
    create_project,
    project_detail,
    skill_search,
    add_skill,
    remove_skill,
    edit_project,
    join_project,
    leave_project,
    close_project,
)

urlpatterns = [
    path("list/", project_list, name="project_list"),
    path("create-project/", create_project, name="create_project"),
    path("<int:project_id>/", project_detail, name="project_detail"),
    path("skills/", skill_search, name="skill_search"),
    path("<int:project_id>/skills/add/", add_skill, name="add_skill"),
    path(
        "<int:project_id>/skills/<int:skill_id>/remove/",
        remove_skill,
        name="remove_skill",
    ),
    path("<int:project_id>/edit/", edit_project, name="edit_project"),
    path("<int:project_id>/join/", join_project, name="join_project"),
    path("<int:project_id>/leave/", leave_project, name="leave_project"),
    path("<int:project_id>/close/", close_project, name="close_project"),
]
