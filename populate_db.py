import os
import django  # type: ignore

from users.models import User
from projects.models import Project, Skill

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "team_finder.settings")
django.setup()


# --- Пользователи ---
users_data = [
    {"email": "mary@yandex.ru", "name": "Мария", "surname": "Трубочева",
     "password": "ADMIN", "phone": "1111111111"},
    {"email": "ivan@yandex.ru", "name": "Иван", "surname": "Иванов",
     "password": "ADMIN", "phone": "2222222222"},
    {"email": "anna@gmail.com", "name": "Анна", "surname": "Окно",
     "password": "ADMIN", "phone": "3333333333"},
    {"email": "petr@yandex.ru", "name": "Петр", "surname": "Петров",
     "password": "ADMIN", "phone": "4444444444"},
]
users = []
for u in users_data:
    user, created = User.objects.get_or_create(email=u["email"], defaults={
        "name": u["name"],
        "surname": u["surname"],
        "phone": u["phone"],
    })
    if created:
        user.set_password(u["password"])
        user.save()
    users.append(user)

# --- Навыки ---
skills_data = ["Python", "Django", "Frontend", "Design"]
skills = []
for name in skills_data:
    skill, _ = Skill.objects.get_or_create(name=name)
    skills.append(skill)

# --- Проекты ---
projects_data = [
    {
        "name": "TeamFinder",
        "description": "Веб-приложение для поиска команды",
        "owner": users[1],
        "status": "open", "skills": ["Python", "Django"]
    },
    {
        "name": "ChatDG",
        "description": "Приложение для чата",
        "owner": users[0], "status": "closed",
        "skills": ["Python", "Frontend"]
    },
    {
        "name": "PortfolioSite",
        "description": "Личный сайт с портфолио",
        "owner": users[1], "status": "open",
        "skills": ["Frontend", "Design"]
    },
]

for p in projects_data:
    project, _ = Project.objects.get_or_create(
        name=p["name"],
        owner=p["owner"],
        defaults={"description": p["description"], "status": p["status"]}
    )
    project.skills.clear()
    for s in p["skills"]:
        skill_obj = Skill.objects.get(name=s)
        project.skills.add(skill_obj)
    project.save()

print("База данных заполнена тестовыми пользователями и проектами!")
