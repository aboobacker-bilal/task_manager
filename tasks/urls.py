from django.urls import path
from .views import (UserTaskList, UserTaskUpdate, TaskReportView,
                    admin_dashboard, task_report, superadmin_dashboard)

urlpatterns = [
    path('tasks/', UserTaskList.as_view(), name='user-tasks'),
    path('tasks/<int:pk>/', UserTaskUpdate.as_view(), name='update-task'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:task_id>/report/', task_report, name='task-report'),
    path('superadmin/', superadmin_dashboard, name='superadmin-dashboard'),
]
