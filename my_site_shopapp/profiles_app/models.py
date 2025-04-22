from django.db import models
from django_resized import ResizedImageField

from auth_app.models import CustomUserModel


def profile_preview_directory_path(instance: "UserProfileModel", filename: str) -> str:
    return f"profiles/profile_{instance.pk}/avatar/{filename}"


class UserProfileModel(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    surname = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(max_length=200, blank=True)

    user = models.OneToOneField(
        CustomUserModel, on_delete=models.CASCADE, related_name="user_profile"
    )
    avatar = ResizedImageField(
        null=True,
        blank=True,
        upload_to=profile_preview_directory_path,
        default="profiles/profile_default/default.png",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"
