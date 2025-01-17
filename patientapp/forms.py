from django import forms
from django.contrib.auth.models import User
from .models import PatientProfile, DoctorProfile, Appointment, MedicalReport


class PatientRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label="Confirm Password",
        required=True
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        required=True
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your date of birth (YYYY-MM-DD)', 'type': 'date'}),
        required=True
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),


        }

        # Password Validation
        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")



class DoctorRegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label="Confirm Password",
        required=True
    )
    speciality = forms.ChoiceField(
        choices=DoctorProfile.SPECIALITY_CHOICES,
        label="Speciality",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    qualification = forms.CharField(
        max_length=100,
        label="Qualification",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your qualification'}),
        required=True
    )

    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),


        }

        # Password Validation
        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")


class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfile
        fields = ['phone_number', 'date_of_birth', 'gender']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter your date of birth', 'type': 'date'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label="Password"
    )


class AppointmentForm(forms.ModelForm):
    speciality = forms.ChoiceField(
        choices=DoctorProfile.SPECIALITY_CHOICES,
        label="Speciality",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.none(),
        label="Doctor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_of_appointment = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date of Appointment"
    )
    time_of_appointment = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label="Time of Appointment"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reason for appointment'}),
        required=False,
        label="Description"
    )

    def __init__(self, *args, **kwargs):
        speciality = kwargs.pop('speciality', None)
        super().__init__(*args, **kwargs)
        if speciality:
            self.fields['doctor'].queryset = DoctorProfile.objects.filter(speciality=speciality)
        else:
            self.fields['doctor'].queryset = DoctorProfile.objects.none()

    class Meta:
        model = Appointment
        fields = ['speciality', 'doctor', 'date_of_appointment', 'time_of_appointment', 'description']


class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['description', 'diagnosis', 'treatment', 'follow_up_instructions', 'file']

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description here'}))
    diagnosis = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter diagnosis here'}))
    treatment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter treatment details here'}))
    follow_up_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter follow-up instructions here'}))
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'application/pdf,image/*'}))

    doctor = forms.ModelChoiceField(queryset=DoctorProfile.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), disabled=True)

    # Adding a read-only field for patient's name
    patient_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        appointment = kwargs.pop('appointment', None)  # Get appointment from the view

        super().__init__(*args, **kwargs)

        if doctor:
            self.fields['doctor'].initial = doctor
            self.fields['doctor'].disabled = True  # Make the doctor field read-only

        if appointment:
            # Set the patient name as the initial value for the patient_name field
            self.fields['patient_name'].initial = appointment.patient.user.get_full_name()
