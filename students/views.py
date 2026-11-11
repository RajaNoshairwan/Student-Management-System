from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Student
from .forms import StudentForm, StudentSearchForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
from django.http import FileResponse
import io
from django.shortcuts import redirect

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    search_form = StudentSearchForm(request.GET)
    students = Student.objects.all()

    if search_form.is_valid():
        roll_number = search_form.cleaned_data.get('roll_number')
        if roll_number:
            students = students.filter(roll_number__icontains=roll_number)

    context = {
        'total_students': total_students,
        'students': students,
        'search_form': search_form,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('dashboard')
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('dashboard')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', 
                 {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('dashboard')
    return render(request, 'students/student_confirm_delete.html', {'student': student})



@login_required
def generate_fee_voucher(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object using ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add content to the PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Student Academy")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 720, "Fee Voucher")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 690, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    p.drawString(50, 670, f"Student Name: {student.name}")
    p.drawString(50, 650, f"Roll Number: {student.roll_number}")
    p.drawString(50, 630, f"Total Fee: ${student.fee_total}")
    p.drawString(50, 610, f"Fee Paid: ${student.fee_paid}")
    p.drawString(50, 590, f"Balance: ${student.fee_total - student.fee_paid}")
    
    # Draw a line
    p.line(50, 580, 550, 580)
    
    p.setFont("Helvetica", 10)
    p.drawString(50, 560, "Please pay the fee at the designated bank within 7 days of issue.")
    
    # Close the PDF object cleanly
    p.showPage()
    p.save()
    
    # FileResponse sets the Content-Disposition header
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'fee_voucher_{student.roll_number}.pdf')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')