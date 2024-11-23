from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.core.MODEL_HANDLER.handlers import upload_csv_path
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['national_id']

    def __str__(self):
        return self.email


class UploadedFile(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='uploaded_files', null=True
    )
    file = models.FileField(upload_to=upload_csv_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmailLog(models.Model):
    template_name = models.CharField(max_length=255)
    to_email = models.EmailField()
    status = models.CharField(max_length=50, choices=[("success", "Success"), ("failed", "Failed")])
    sent_at = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.to_email} - {self.template_name} - {self.status}"


from django.db import models


class BulkEmailTask(models.Model):
    task_id = models.CharField(max_length=255)
    template_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ("active", "Active"),
        ("paused", "Paused"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.template_name} - {self.status} - {self.progress}%"
