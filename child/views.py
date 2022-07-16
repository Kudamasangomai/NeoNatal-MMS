from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q ,Count
from django.views.generic import (

ListView,
DetailView,
FormView,
UpdateView ,
DeleteView,CreateView
)

from .models import child 
from patients.models import *
from main.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from sendsms.message import SmsMessage
from django.conf import settings

class ChildListView(LoginRequiredMixin, ListView):
    model = child
    template_name = 'child/childlist.html'
    context_object_name = 'children'

class ChildDetailedView(LoginRequiredMixin,DetailView):
    model = child
    template_name = 'child/child-detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['othertest'] = childtest.objects.filter(child_regno = self.object.childregno)
        ctx['xyz'] = child.objects.values('agparscore').annotate(count=Count('agparscore'))
        ctx['abc'] = childtest.objects.values('agpar_score').annotate(count=Count('agpar_score'))
        ctx['agpar_score_count'] =childtest.objects.filter(Q(child_regno = self.object.childregno) & Q( agpar_score__gte=7)).count()
        ctx['agparscore_count'] =child.objects.filter(Q(childregno = self.object.childregno) & Q( agparscore__gte=7)).count()
        ctx['heart_rate_count'] =childtest.objects.filter(Q(child_regno = self.object.childregno) & Q( heart_rate__gte=1)).count()
        ctx['heartrate_count'] =child.objects.filter(Q(childregno = self.object.childregno) & Q( heartrate__gte=1)).count()
        ctx['agpar_result'] = (ctx['agpar_score_count'] + ctx['agparscore_count'])
        ctx['heart_rate_result'] = (ctx['heart_rate_count'] + ctx['heartrate_count'])
        return ctx

class AddChildview(LoginRequiredMixin, SuccessMessageMixin,CreateView):
    model = child
    form_class = Addchildform
    template_name = 'child/addchild.html'
    success_url = reverse_lazy('patients')
    success_message = 'child Added Successfully'

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['motherinfo'] = patient.objects.get(id=self.kwargs['pk'])
        return ctx

    def form_valid(self,form):
        motherid = patient.objects.get(id=self.kwargs['pk'])    
        form.instance.motherid = motherid
        form.instance.nurseincharge = self.request.user
        return super().form_valid(form)

class  AddTestview(LoginRequiredMixin, SuccessMessageMixin,CreateView):
    model = childtest
    form_class = Addchildtestform
    template_name = 'child/addchildtest.html'
    success_url = reverse_lazy('child-list')

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['childregno'] = child.objects.get(childregno=self.kwargs['childregno'])
        return ctx
    

    def form_valid(self,form):
        child_regno = child.objects.get(childregno =self.kwargs['childregno'])    
        form.instance.child_regno = child_regno.childregno
        return super().form_valid(form)


def sendmsg(request):
    # frm = '+263777696355'
    # to = '+263718354315'
    # text = 'Please remember to pick up the bread before coming'
   
    # message = SmsMessage(body='lolcats make me hungry', from_phone='+263777696355', to=['+263718354315'])
    # message.send()
    from sendsms import api
    api.send_sms(body='I can haz txt', from_phone='+263777696355', to=['+263718354315'])