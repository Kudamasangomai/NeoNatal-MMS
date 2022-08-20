from django.urls import path

from patients.models import patient
from . import views


from .views import (



   UpdatepatientView,
   patientslistview,
   patientdetail,
   AddPatientView,
   DeletePatientView,
   AddMedcialRecordView,
   AssignNurseView,
   ViewChildrenView,

	 )




urlpatterns = [    

  


   path('patients/',patientslistview.as_view(),name="patients"),
   path('patientdetail/<int:pk>',patientdetail.as_view(),name="patient-detail"),
   path('patient/addpatients/',AddPatientView.as_view(),name="add-patient"),
   path('patient/delete/<int:pk>',DeletePatientView.as_view(),name="delete-patient"),
   path('patient/update/<int:pk>/', UpdatepatientView.as_view(),name="patient-update"),

   path('htmx/patientdetail/<pk>/delete/', views.delete_medical_record, name="delete-medical-record"),
   path('patient/addmedicalrecord/<int:pk>/',AddMedcialRecordView.as_view(),name="add-medical-record"), 

   path('patient_children/<int:pk>',ViewChildrenView.as_view(),name="view-children"),

   path('assignurset/<int:pk>/',views.assignurset,name="assignurset"),
   path('assign/<int:pk>/',views.AssignNurseView,name="assign-nurse"),

   path('export_csv/',views.export_csv,name="export-csv"),
   path('export_pdf/',views.export_pdf,name="export-pdf"),

  
   
  
]

