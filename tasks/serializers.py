from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ["assigned_to", "completion_report", "worked_hours"]

    def get_user_roles(self, obj):
        return [group.name for group in obj.assigned_to.groups.all()]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["status", "completion_report", "worked_hours"]

    def validate(self, data):
        if data.get("status") == "completed":
            if not data.get('completion_report') or data.get("worked_hours") is None:
                raise serializers.ValidationError(
                    "Report and work hours required to mark as completed."
                )
        return data
