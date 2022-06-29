from django.urls import path

from patients.models import patient
from . import views


from .views import (


#   addpatients,
 #  UpdatepatientView,
   patientslistview,
   patientdetail,
   AddPatientView,
   AddMedcialRecordView,
   AssignNurseView,

	 )




urlpatterns = [    

  


   path('patients/',patientslistview.as_view(),name="patients"),
   path('patientdetail/<int:pk>',patientdetail.as_view(),name="patient-detail"),
   path('patients/addpatients/',AddPatientView.as_view(),name="add-patient"),
#    path('userdetail/<int:pk>/', UpdatepatientView.as_view(),name="user-detail"),
#    path('users/update/<int:pk>/', UpdatepatientView.as_view(),name="user-update"),



 path('patients/addmedicalrecord/<int:pk>/',AddMedcialRecordView.as_view(),name="add-medical-record"),
 path('assignurset/<int:pk>/',views.assignurset,name="assignurset"),
path('assign/<int:pk>/',views.AssignNurseView,name="assign-nurse")

  
   
  
]

