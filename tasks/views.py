from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from rest_framework.exceptions import PermissionDenied


class UserTaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class UserTaskUpdate(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task = Task.objects.get(pk=self.kwargs['pk'])

        if task.status != "completed":
            raise PermissionDenied("Task not yet completed.")
        user = self.request.user
        if not (
                user.is_superuser or user.is_staff or
                user.groups.filter(name__in=["Admin", "SuperAdmin"]).exists()
        ):
            raise PermissionDenied(
                "Only Admins and SuperAdmins can view reports."
            )
        return task
