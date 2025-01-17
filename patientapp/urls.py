from django.urls import path
from . import views
from .views import view_medical_reports

urlpatterns = [

    path('', views.home, name='home'),

    # Admin urls
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    #Manage patients
    path('admin_patients/', views.admin_patients, name='admin_patients'),
    path('admin_patient_view/<int:patient_id>/', views.view_patient, name='view_patient'),
    path('admin_patient_delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('admin_patient_medical_report/<int:patient_id>/', views.view_medical_report_admin, name='view_medical_report_admin'),

    #Manage doctors
    path('admin_doctors/', views.admin_doctors, name='admin_doctors'),
    path('admin_doctor_view/<int:doctor_id>/', views.view_doctor, name='view_doctor'),
    path('admin_doctor_delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

    #Manage appointments
    path('admin_appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin_appointment_view/<int:appointment_id>/', views.view_appointment, name='view_appointment'),
    path('admin_appointment_update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),



    # Doctor urls
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_registration/', views.register_doctor, name='doctor_registration'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('add-medical-report/<int:appointment_id>/', views.add_medical_report, name='add_medical_report'),
    path('medical-reports/<int:patient_id>/', view_medical_reports, name='view_medical_reports'),


    # Patient urls
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient_registration/', views.register_patient, name='patient_registration'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('view-profile/', views.view_profile, name='view_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),

    path('make-appointment/',views.make_appointment, name = 'make_appointment'),
    path('appointment/payment/<int:appointment_id>/', views.make_payment, name='make_payment'),
    path('payment/success/<int:appointment_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:appointment_id>/', views.payment_cancel, name='payment_cancel'),

    path('get-doctors/', views.get_doctors, name='get_doctors'),
    path('view-medical-reports/', view_medical_reports, name='view_medical_reports'),



    path('logout/', views.logout, name='logout'),
]
