import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from .forms import PatientRegistrationForm, LoginForm, PatientProfileForm, DoctorRegistrationForm, AppointmentForm, \
    MedicalReportForm
from .models import PatientProfile, DoctorProfile, Appointment, MedicalReport
from django.http import JsonResponse, HttpResponseForbidden


def home(request):

    return render(request, 'home.html')

@never_cache
def logout(request):
    logout(request)
    request.session.flush()
    return redirect('home')



# ADMIN
def admin_login(request):


    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:  # Ensure only staff users can log in
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, "Invalid credentials or not an admin")

    return render(request, 'admin/admin_login.html', {"form": form})

def is_admin_or_staff(user):
    return user.is_authenticated and user.is_staff  # Ensures only staff users can access

@login_required(login_url='/admin-login/')
@user_passes_test(is_admin_or_staff)
@never_cache
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required
@user_passes_test(is_admin_or_staff)
def admin_patients(request):
    # Get all patients
    patients = PatientProfile.objects.all()
    return render(request, 'admin/manage_patients.html', {'patients': patients})

@login_required
@user_passes_test(is_admin_or_staff)
def view_patient(request, patient_id):
    # View patient registration details
    patient = get_object_or_404(PatientProfile, id=patient_id)
    return render(request, 'admin/view_patient_details.html', {'patient': patient})

@login_required
@user_passes_test(is_admin_or_staff)
def delete_patient(request, patient_id):
    # Delete a patient
    patient = get_object_or_404(PatientProfile, id=patient_id)
    patient.delete()
    return redirect('admin_patients')

@login_required
@user_passes_test(is_admin_or_staff)
def view_medical_report_admin(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(PatientProfile, id=patient_id)
    # Fetch all medical reports for the patient
    reports = MedicalReport.objects.filter(patient=patient)

    return render(request, 'admin/view_medical_report.html', {'patient': patient, 'reports': reports})

@login_required
@user_passes_test(is_admin_or_staff)
def admin_doctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'admin/manage_doctors.html', {'doctors': doctors})

@login_required
@user_passes_test(is_admin_or_staff)
def view_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    return render(request, 'admin/view_doctor_details.html', {'doctor': doctor})

@login_required
@user_passes_test(is_admin_or_staff)
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor.user.delete()  # Deletes associated user and doctor profile
    return redirect('admin_doctors')

@login_required
@user_passes_test(is_admin_or_staff)
def admin_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/manage_appointments.html', {'appointments': appointments})

@login_required
@user_passes_test(is_admin_or_staff)
def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'admin/view_appointment_details.html', {'appointment': appointment})

@login_required
@user_passes_test(is_admin_or_staff)
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        appointment.date_of_appointment = request.POST.get("date_of_appointment")
        appointment.time_of_appointment = request.POST.get("time_of_appointment")
        appointment.save()
        return redirect("admin_appointments")

    return render(request, "admin/update_appointment.html", {"appointment": appointment})



# PATIENT
def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            phone_number = form.cleaned_data['phone_number']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']

            PatientProfile.objects.create(user=user, phone_number=phone_number, date_of_birth=date_of_birth, gender=gender)

            return redirect('patient_login')
    else:
        form = PatientRegistrationForm()

    return render(request,'patient/register_patient.html',{'form':form})


def patient_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('patient_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'patient/patient_login.html', {'form': form})

def is_patient(user):
    return hasattr(user, 'patientprofile')

@login_required(login_url='/patient-login/')
@user_passes_test(is_patient)
@never_cache
def patient_dashboard(request):

    return render(request, 'patient/patient_dashboard.html')

@login_required
@user_passes_test(is_patient)
def update_profile(request):
    profile, _ = PatientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = PatientProfileForm(instance=profile)
    return render(request, 'patient/update_profile.html', {'form': form})

@login_required
@user_passes_test(is_patient)
def view_profile(request):
    profile = PatientProfile.objects.get(user=request.user)
    return render(request, 'patient/view_profile.html', {'profile': profile})


@login_required
@user_passes_test(is_patient)
def get_doctors(request):
    speciality = request.GET.get('speciality')
    doctors = DoctorProfile.objects.filter(speciality=speciality)
    doctor_list = [
        {
            'id': doctor.id,
            'first_name': doctor.user.first_name,
            'last_name': doctor.user.last_name,
        }
        for doctor in doctors
    ]
    return JsonResponse({'doctors': doctor_list})

@login_required
@user_passes_test(is_patient)
def make_appointment(request):
    # Get the logged-in user's patient profile
    patient_profile = PatientProfile.objects.get(user=request.user)

    if request.method == 'POST':
        speciality = request.POST.get('speciality')  # Get the selected speciality
        form = AppointmentForm(request.POST, speciality=speciality)  # Pass speciality to the form

        if form.is_valid():
            # Save the appointment and link it to the logged-in patient
            appointment = form.save(commit=False)
            appointment.patient = patient_profile
            appointment.save()
            # messages.success(request, "Your appointment was successfully created!")
            return redirect('make_payment', appointment_id=appointment.id)  # Replace with your success page URL name
    else:
        form = AppointmentForm()

    return render(request, 'patient/appointment.html', {'form': form})


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@user_passes_test(is_patient)
def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patientprofile)

    if appointment.payment_status == 'Completed':
        messages.info(request, "Payment for this appointment has already been completed.")
        return redirect('patient_dashboard')

    if request.method == 'POST':
        try:
            # Create a Stripe payment session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f"Appointment with Dr. {appointment.doctor.user.first_name}",
                            },
                            'unit_amount': 500,  # $50.00
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(f'/payment/success/{appointment.id}/'),
                cancel_url=request.build_absolute_uri(f'/payment/cancel/{appointment.id}/'),
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('make_payment', appointment_id=appointment.id)

    return render(request, 'patient/payment.html', {
        'appointment': appointment,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
@user_passes_test(is_patient)
def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patientprofile)
    appointment.payment_status = 'Paid'
    appointment.save()
    messages.success(request, "Payment successful! Your appointment is confirmed.")
    return redirect('patient_dashboard')

@login_required
@user_passes_test(is_patient)
def payment_cancel(request, appointment_id):
    messages.error(request, "Payment was canceled. Please try again.")
    return redirect('make_payment', appointment_id=appointment_id)


@login_required
@user_passes_test(is_patient)
def view_medical_reports(request, patient_id=None):
    # Ensure the logged-in user is either a patient or a doctor
    if hasattr(request.user, 'patientprofile'):
        # If logged-in user is a patient, show only their own reports
        patient = request.user.patientprofile
        reports = MedicalReport.objects.filter(patient=patient)
        return render(request, 'patient/view_medical_report.html', {'reports': reports, 'patient': patient})

    elif hasattr(request.user, 'doctorprofile'):
        # If logged-in user is a doctor, allow access to a specific patient's reports
        if patient_id:
            patient = get_object_or_404(PatientProfile, id=patient_id)
            reports = MedicalReport.objects.filter(patient=patient)
            return render(request, 'doctor/view_medical_report.html', {'reports': reports, 'patient': patient})
        else:
            return HttpResponseForbidden("You are not allowed to view this content.")
    else:
        return HttpResponseForbidden("You are not allowed to view this content.")





# DOCTOR
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            speciality = form.cleaned_data['speciality']
            qualification = form.cleaned_data['qualification']
            phone_number = form.cleaned_data['phone_number']

            DoctorProfile.objects.create(user=user, speciality=speciality, qualification=qualification, phone_number=phone_number)

            return redirect('doctor_login')
    else:
        form = DoctorRegistrationForm()

    return render(request,'doctor/register_doctor.html',{'form':form})


def doctor_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'doctor/doctor_login.html', {'form': form})

def is_doctor(user):
    return hasattr(user, 'doctorprofile')

@login_required(login_url='/doctor-login/')
@user_passes_test(is_doctor)
@never_cache
def doctor_dashboard(request):

    doctor_profile = DoctorProfile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor_profile)

    return render(request, 'doctor/doctor_dashboard.html', {'appointments': appointments})

@login_required
@user_passes_test(is_doctor)
def accept_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'Accepted'  # Now you can set the status field
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
@user_passes_test(is_doctor)
def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('doctor_dashboard')

@login_required
@user_passes_test(is_doctor)
def add_medical_report(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    patient = appointment.patient
    doctor = request.user.doctorprofile  # Get the logged-in doctor's profile

    if request.method == 'POST':
        form = MedicalReportForm(request.POST, request.FILES, doctor=doctor, appointment=appointment)  # Pass both doctor and appointment to the form
        if form.is_valid():
            # Create and save the medical report
            medical_report = form.save(commit=False)
            medical_report.appointment = appointment
            medical_report.patient = patient
            medical_report.doctor = doctor
            medical_report.save()
            return redirect('doctor_dashboard')
    else:
        form = MedicalReportForm(doctor=doctor, appointment=appointment)  # Pass both doctor and appointment on GET request

    return render(request, 'doctor/add_medical_report.html', {'form': form, 'appointment': appointment, 'patient': patient})
