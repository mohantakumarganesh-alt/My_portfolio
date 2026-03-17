from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from .models import Student, Grade, Attendance, Course
from .forms import StudentForm

class DashboardView(TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.count()
        context['total_courses'] = Course.objects.count()
        context['avg_grade'] = Grade.objects.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0.0
        
        # Aggregate data for Chart.js
        genders = Student.objects.values('gender').annotate(count=Count('gender'))
        gender_map = {'M': 'Male', 'F': 'Female', 'O': 'Other'}
        context['gender_stats_labels'] = [gender_map.get(g['gender'], 'Other') for g in genders]
        context['gender_stats_values'] = [g['count'] for g in genders]
        
        # Recent Students list
        context['recent_students'] = Student.objects.order_by('-created_at')[:5]
        
        return context

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
