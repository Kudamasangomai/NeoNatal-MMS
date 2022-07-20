
from patients.models import *
from django.contrib.auth.models import User 


def my_total_patients(request,**kwargs):
    my_patients_details = patient.objects.filter(patient_assignednurse = request.user.id)
    my_total_patients = patient.objects.filter(patient_assignednurse = request.user.id).count()
    return {
        'my_total_patients':my_total_patients,
        'my_patients_details':my_patients_details
        }