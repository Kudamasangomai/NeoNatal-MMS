from django.shortcuts import render
from django.views.generic import (

ListView,
DetailView,
FormView,
UpdateView ,
DeleteView,CreateView
) 


class AddChildview(CreateView):
    model: child
   

