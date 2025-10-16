from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.username} ({self.organization})"



class File(models.Model):
    """
    Each file belongs to an organization by the uploaded_by user.
    User and Files belong to Organization (null=False, blank=False).
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="files"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.organization})"

class Download(models.Model):
    """
    Model to track file downloads by users.
    Download belongs to an organization via the user and file.
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="downloads",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="downloads",
    )
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name="downloads",
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.file}"