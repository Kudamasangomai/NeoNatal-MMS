from django.urls import path
from . import views


from .views import (

AddChildview

	 )




urlpatterns = [    

  


   path('patient/add_child/',AddChildview.as_view(),name="add-child"),



  
   
  
]

