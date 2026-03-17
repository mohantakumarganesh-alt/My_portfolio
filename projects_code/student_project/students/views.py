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

from django.views.generic import DetailView

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        
        # Stats Aggregates
        context['avg_grade'] = student.grades.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0.0
        
        total_days = student.attendance.count()
        present_days = student.attendance.filter(is_present=True).count()
        context['attendance_rate'] = (present_days / total_days * 100) if total_days > 0 else 100.0
        
        # Chart Data
        grades = student.grades.select_related('course')
        context['grade_labels'] = [g.course.name for g in grades]
        context['grade_values'] = [float(g.marks_obtained) for g in grades]
        
        return context

from django.utils import timezone

class BulkAttendanceView(TemplateView):
    template_name = 'students/attendance_bulk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        context['today'] = timezone.now().date()
        return context

    def post(self, request, *args, **kwargs):
        date_str = request.POST.get('date')
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
        present_ids = request.POST.getlist('present_students')
        
        all_students = Student.objects.all()
        for student in all_students:
            is_present = str(student.id) in present_ids
            Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'is_present': is_present}
            )
            
        context = self.get_context_data(**kwargs)
        context['today'] = date
        context['success_message'] = 'Attendance recorded successfully!'
        return render(request, self.template_name, context)

import csv
from django.http import HttpResponse

def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Roll No', 'Name', 'Email', 'Gender', 'Contact', 'DOB'])

    from .models import Student
    students = Student.objects.all()
    for s in students:
        writer.writerow([s.roll_no, s.name, s.email, s.get_gender_display(), s.contact, s.dob])

    return response
