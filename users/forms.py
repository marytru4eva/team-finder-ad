from django import forms

from users.models import User


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = User
        fields = ("name", "surname", "email", "phone")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "name",
            "surname",
            "email",
            "phone",
            "avatar",
            "github_url",
            "about",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False
        self.fields["avatar"].required = False
        self.fields["github_url"].required = False
        self.fields["about"].required = False

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")

        if not github_url:
            return github_url

        if "github.com" not in github_url:
            raise forms.ValidationError("Ссылка должна вести на GitHub.")

        return github_url
