# students/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_admission = models.DateField()
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fee_total = models.DecimalField(max_digits=10, decimal_places=2)
    attendance_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    class Meta:
        ordering = ['-date_of_admission']