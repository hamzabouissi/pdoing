from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pdoing.core.Base import BaseModel


class UserTypeEnum(models.TextChoices):
    Developer = "Dev", _("Developer")
    Instructor = "Inst", _("Instructor")


class User(AbstractUser):
    """Default user for PDoing."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(
        _("email address"),
        blank=False,
        null=False,
        default="testuser@gmail.com",
        unique=True,
    )
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    user_type = models.CharField(
        max_length=20, choices=UserTypeEnum.choices, default=UserTypeEnum.Developer
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Profile(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    programming_languages = models.CharField(max_length=100, default="")
    project_themes = models.CharField(max_length=100, default="")
    badges = models.CharField(max_length=25)  # todo change
