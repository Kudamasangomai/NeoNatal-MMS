from django.urls import path
from . import views


from .views import (

AddChildview,
ChildListView,
ChildDetailedView,
AddTestview
	 )




urlpatterns = [    

  

   path('children',ChildListView.as_view(),name="child-list"),
   path('add_child/<int:pk>/',AddChildview.as_view(),name="add-child"),
    path('add_child_test/<childregno>/',AddTestview.as_view(),name="add-test"),
   path('child_detail/<int:pk>',ChildDetailedView.as_view(),name="child-detail"),
  # path('patients/addmedicalrecord/<int:pk>/',AddMedcialRecordView.as_view(),name="add-medical-record"),
  path('child/sendmsg',views.sendmsg,name="send-msg")


  
   
  
]

