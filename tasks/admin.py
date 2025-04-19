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
    list_display = ("title", "assigned_to", "get_user_role", "status")
    list_filter = ("status", "due_date", "assigned_to")
    search_fields = ("title", "description", "assigned_to__username")
    readonly_fields = ["completion_report", "worked_hours"]

    def get_user_role(self, obj):
        return obj.assigned_to.role

    get_user_role.short_description = "User Role"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "role", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
