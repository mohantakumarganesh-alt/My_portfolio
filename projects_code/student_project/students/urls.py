from django.urls import path
from .views import DashboardView, StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView, StudentDetailView, BulkAttendanceView, export_students_csv

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/add/', StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('attendance/', BulkAttendanceView.as_view(), name='attendance_bulk'),
    path('students/export/', export_students_csv, name='export_students_csv'),
]
