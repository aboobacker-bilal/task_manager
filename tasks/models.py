from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass
    # ROLE_CHOICES = (
    #     ('superadmin', 'SuperAdmin'),
    #     ('admin', 'Admin'),
    #     ('user', 'User'),
    # )
    # role = models.CharField(
    #     max_length=20, choices=ROLE_CHOICES, default='user'
    # )
    #
    # def __str__(self):
    #     return f"{self.username} ({self.role})"


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='tasks'
    )
    due_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    completion_report = models.TextField(blank=True)
    worked_hours = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} {self.assigned_to.username} {self.status}"
