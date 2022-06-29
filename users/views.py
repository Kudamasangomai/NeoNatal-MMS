from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required , permission_required
from main.forms import AddUserForm 
from django.contrib import messages
from django.views.generic import ListView,DetailView,FormView,UpdateView ,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

# from django.views import View
# #works with function based views
# 
# #works with class based viewws

# from django.views.generic.edit import CreateView
#
# 
# 
# from library.models import issuedbooks ,reservedbooks
# from django.utils.timesince import timesince
# from datetime import datetime,timedelta
# from django.utils import timezone

#import requests
# Create your views here.
class userslistview(ListView):

	model = User
	template_name = 'users/users.html'
	context_object_name = 'users'
	paginate_by =  10


class UserDetailView(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'users/userdetail.html'
	context_object_name = 'usersinfo'

class  UpdateUserView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/register.html'
    fields = ['first_name','last_name','username','email','is_staff']
    success_url = reverse_lazy('users')
    success_message = "Category Successfully Updated"



@login_required
def adduser(request):
    if request.method == 'POST':
      form =  AddUserForm(request.POST)

    
      if form.is_valid():
             form.save()
          
             username = form.cleaned_data.get('username')
             messages.success(request, f'Account for {username} has been Successfully Created')
             return redirect('users')
    else:
        form = AddUserForm()
    return render(request ,'users/register.html',{'form':form})
