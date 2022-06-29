from django.urls import path
from . import views
#from library.forms import AddUserForm
from django.contrib.auth import views as auth_views
from .views import (

# 	forgotpassword,
# 	adduser,
 	userslistview,
   UserDetailView,
#    UserAccountListView
   UpdateUserView

	 )




urlpatterns = [    

  

   #path('forgotpassword',forgotpassword.as_view(),name="forgot-password"),
   path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "users/reset_password.html"), name ='reset_password'),
   path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name ='password_reset_done'),
   path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name ='password_reset_confirm'),
   path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name ='password_reset_complete'),

   # path('profile/',views.profile,name="profile"),  
   # path('users/profile_edit/<int:pk>',views.profile_edit,name="profile-edit"),
   path('users/',userslistview.as_view(),name="users"),
   path('users/adduser/',views.adduser,name="add-user"),
   path('userdetail/<int:pk>/',UserDetailView.as_view(),name="user-detail"),
   path('users/update/<int:pk>/',UpdateUserView.as_view(),name="user-update"),
   # path('user_account/',UserAccountListView.as_view(),name='user-account')


  
   
  
]

