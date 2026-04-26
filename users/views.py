from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserForm, UserRegisterForm
from users.models import User


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "users/user-details.html", {"profile_user": user})


def register(request):
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("project_list")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    error = ""

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("project_list")

        error = "Неверный email или пароль"

    return render(request, "users/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("project_list")


def users_list(request):
    users = User.objects.all().order_by("name", "surname")
    return render(request, "users/users_list.html", {"users": users})


@login_required
def edit_profile(request):
    form = UserForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )

    if form.is_valid():
        form.save()
        return redirect("users:edit_profile")

    return render(request, "users/edit_profile.html", {"form": form})
