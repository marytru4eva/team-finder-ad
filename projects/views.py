from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from projects.constants import (
    PROJECTS_PER_PAGE,
    SKILL_SEARCH_LIMIT,
    STATUS_CLOSED,
    STATUS_OPEN,
)
from projects.forms import ProjectForm
from projects.models import Project, Skill


def project_list(request):
    skill_name = request.GET.get("skill")
    projects = (
        Project.objects.prefetch_related("participants", "skills")
        .select_related("owner")
        .order_by("-created_at")
    )

    if skill_name:
        projects = projects.filter(skills__name__iexact=skill_name)

    all_skills = Skill.objects.all().order_by("name")

    paginator = Paginator(projects, PROJECTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page_obj,
            "all_skills": all_skills,
            "active_skill": skill_name,
        },
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("participants", "skills")
        .select_related("owner"),
        id=project_id,
    )
    all_skills = Skill.objects.all().order_by("name")

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "all_skills": all_skills,
        },
    )


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        form.save_m2m()
        project.participants.add(request.user)
        return redirect("project_detail", project_id=project.id)

    return render(
        request,
        "projects/create_project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner"),
        id=project_id,
    )
    if request.user != project.owner:
        return redirect("project_list")

    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect("project_detail", project_id=project.id)

    return render(
        request,
        "projects/edit_project.html",
        {"form": form, "project": project},
    )


def skill_search(request):
    query = request.GET.get("q", "")
    skills = Skill.objects.filter(
        name__istartswith=query,
    ).order_by("name")[:SKILL_SEARCH_LIMIT]

    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
def add_skill(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        return redirect("project_detail", project_id=project.id)

    if request.method == "POST":
        skill_id = request.POST.get("skill_id")

        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)
            project.skills.add(skill)

    return redirect("project_detail", project_id=project.id)


@login_required
def remove_skill(request, project_id, skill_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        return redirect("project_detail", project_id=project.id)

    if request.method == "POST":
        skill = get_object_or_404(Skill, id=skill_id)
        project.skills.remove(skill)

    return redirect("project_detail", project_id=project.id)


@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        if project.status == STATUS_OPEN and request.user != project.owner:
            project.participants.add(request.user)

    return redirect("project_detail", project_id=project.id)


@login_required
def leave_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST" and request.user != project.owner:
        project.participants.remove(request.user)

    return redirect("project_detail", project_id=project.id)


@login_required
def close_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        return redirect("project_detail", project_id=project.id)

    if request.method == "POST" and project.status == STATUS_OPEN:
        project.status = STATUS_CLOSED
        project.save()

    return redirect("project_detail", project_id=project.id)
