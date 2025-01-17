from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now


class PatientProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=False)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])


    def __str__(self):
        return self.user.username


class DoctorProfile(models.Model):

    SPECIALITY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('General Medicine', 'General Medicine'),
        ('Gynecology', 'Gynecology'),
        ('Psychiatry', 'Psychiatry'),
        ('Radiology', 'Radiology'),

    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100, choices=SPECIALITY_CHOICES,)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    date_of_appointment = models.DateField(default=timezone.now)
    time_of_appointment = models.TimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted')], default='Pending')
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.first_name} by {self.patient.user.first_name} on {self.date_of_appointment}"


class MedicalReport(models.Model):

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    description = models.TextField()
    diagnosis = models.CharField(max_length=255, null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    follow_up_instructions = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='medical_reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient.user.first_name} by Dr. {self.doctor.user.first_name}"