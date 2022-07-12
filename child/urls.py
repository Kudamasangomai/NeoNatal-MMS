from django.urls import path
from . import views


from .views import (

AddChildview,
ChildListView
	 )




urlpatterns = [    

  

   path('',ChildListView.as_view(),name="child-list"),
   path('add_child/<int:pk>/',AddChildview.as_view(),name="add-child"),
  # path('patients/addmedicalrecord/<int:pk>/',AddMedcialRecordView.as_view(),name="add-medical-record"),


  
   
  
]

