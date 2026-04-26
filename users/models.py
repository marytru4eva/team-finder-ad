import io
import random

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from users.constants import (
    ABOUT_MAX_LENGTH,
    AVATAR_ANCHOR,
    AVATAR_COLORS,
    AVATAR_FORMAT,
    AVATAR_SIZE,
    NAME_MAX_LENGTH,
    PHONE_MAX_LENGTH,
)
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Имя")
    surname = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Телефон",
    )
    github_url = models.URLField(blank=True, verbose_name="GitHub")
    about = models.CharField(
        max_length=ABOUT_MAX_LENGTH,
        blank=True,
        verbose_name="О себе",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("name", "surname")

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        background_color = random.choice(AVATAR_COLORS)

        image = Image.new("RGB", AVATAR_SIZE, background_color)
        draw = ImageDraw.Draw(image)

        first_letter = (self.name[:1] if self.name else self.email[:1]).upper()
        font = ImageFont.load_default()

        bbox = draw.textbbox(AVATAR_ANCHOR, first_letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (AVATAR_SIZE[0] - text_width) / 2
        y = (AVATAR_SIZE[1] - text_height) / 2

        draw.text((x, y), first_letter, fill="white", font=font)

        buffer = io.BytesIO()
        image.save(buffer, format=AVATAR_FORMAT)

        file_name = (
            f"avatar_{self.email.replace('@', '_').replace('.', '_')}.png"
        )

        self.avatar.save(
            file_name,
            ContentFile(buffer.getvalue()),
            save=False,
        )
