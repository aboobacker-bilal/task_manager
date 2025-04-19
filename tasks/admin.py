from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms

from .models import Task, CustomUser
from django.contrib.auth.admin import UserAdmin


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        report = cleaned_data.get('completion_report')
        hours = cleaned_data.get('worked_hours')

        if status == 'completed':
            if not report:
                raise ValidationError("Completion report is required when task is completed.")
            if hours is None:
                raise ValidationError("Worked hours are required when task is completed.")
        return cleaned_data


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm

    def get_user_groups(self, obj):
        return ", ".join([group.name for group in obj.assigned_to.groups.all()])

    get_user_groups.short_description = "User Role"

    list_display = ("title", "assigned_to", "status")
    list_filter = ("status", "due_date", "assigned_to")
    search_fields = ("title", "description", "assigned_to__username")
    readonly_fields = ["completion_report", "worked_hours"]


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
