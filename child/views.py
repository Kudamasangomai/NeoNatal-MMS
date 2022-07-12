from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (

ListView,
DetailView,
FormView,
UpdateView ,
DeleteView,CreateView
)

from .models import child 
from main.forms import *
from django.contrib.messages.views import SuccessMessageMixin


class ChildListView(ListView):
    template_name: str

class AddChildview(SuccessMessageMixin,CreateView):
    model: child
    form_class: Addchildform
    template_name = 'child/addchild.html'
    success_url = reverse_lazy('patients')
    success_message = 'child Added'


