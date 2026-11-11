# students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'phone_number', 'date_of_admission', 
                 'fee_paid', 'fee_total', 'attendance_percentage']
        widgets = {
            'date_of_admission': forms.DateInput(attrs={'type': 'date'}),
        }

class StudentSearchForm(forms.Form):
    roll_number = forms.CharField(required=False, max_length=20)