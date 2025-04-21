from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from rest_framework.exceptions import PermissionDenied


class UserTaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)


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
        if self.request.user.role not in ["admin", "superadmin"]:
            raise PermissionDenied(
                "Only admins and superadmins can view reports."
            )
        return task


@login_required
@login_required
def admin_dashboard(request):
    if request.user.role == 'admin':
        tasks = Task.objects.filter(assigned_to__admin=request.user)
        return render(request, 'admin_dashboard.html', {'tasks': tasks})


@login_required
def task_report(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status != 'completed':
        return HttpResponseForbidden("This task is not completed yet.")

    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        return HttpResponseForbidden("You do not have permission to view")

    return render(request, 'reports.html', {'task': task})


User = get_user_model()


def is_superadmin(user):
    return user.is_authenticated and user.role == 'superadmin'


@login_required
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    users = User.objects.exclude(id=request.user.id)
    admins = User.objects.filter(role='admin')
    regular_users = User.objects.filter(role='user')
    return render(request, 'sa_dashboard.html', {
        'users': users,
        'admins': admins,
        'regular_users': regular_users
    })


@login_required
@user_passes_test(is_superadmin)
def assign_user_to_admin(request, user_id):
    user = get_object_or_404(User, id=user_id, role='user')
    admins = User.objects.filter(role='admin')
    if request.method == 'POST':
        admin_id = request.POST.get('admin')
        admin = get_object_or_404(User, id=admin_id)
        user.admin = admin
        user.save()
        return redirect('superadmin-dashboard')
    return render(request, 'assign_user.html', {
            'user': user, 'admins': admins
        })
