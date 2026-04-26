from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url"]

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")

        if not github_url:
            return github_url

        validator = URLValidator()

        try:
            validator(github_url)
        except ValidationError as error:
            raise forms.ValidationError("Введите корректный URL.") from error

        if "github.com" not in github_url:
            raise forms.ValidationError("Ссылка должна вести на GitHub.")

        return github_url
