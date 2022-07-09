from django.views.generic import (

ListView,
DetailView,
FormView,
UpdateView ,
DeleteView,CreateView
) 
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,redirect
from .models import patient ,medical_record
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q ,Count
from django.contrib import messages
from main.forms import *



# Create your views here.


class patientslistview(ListView):
    model = patient
    template_name = 'patients/patientslist.html'
    context_object_name = 'patients'
    paginate_by =  10
    

    def get_context_data(self, **kwargs):
        context = super(patientslistview,self).get_context_data(**kwargs)
        #context['patients'] = patient.objects.all()
        context['assignednurse'] = User.objects.all()
        return context


class patientdetail(DetailView):
    model= patient
    template_name =  'patients/patientdetail.html'
    context_object_name = 'patientdetail'

    def get_context_data(self,**kwargs):
        context = super(patientdetail, self).get_context_data(**kwargs)
        context['medical_record'] = medical_record.objects.filter(patientid=self.kwargs['pk'])
        context['qs'] = User.objects.all()
        #context['hbccount'] = medical_record.objects.values('hbc').annotate(count=Count('hbc'))
        context['hbccount'] = medical_record.objects.filter(patientid = self.kwargs['pk']).count()
        context['normalhbc'] = medical_record.objects.filter(Q(patientid = self.kwargs['pk']) & Q( hbc__gte=11)).count()
        context['notnormalhbc'] = medical_record.objects.filter(Q(patientid = self.kwargs['pk']) & Q( hbc__lte=11)).count()
        context['survival'] = ((context['normalhbc'] / context['hbccount']) * 100)
        context['nochancesurvival'] = ((context['notnormalhbc'] / context['hbccount']) * 100)
        return context


class AddPatientView(SuccessMessageMixin,CreateView):
    model = patient
    form_class = AddPatientForm
    template_name = 'patients/addpatients.html'
    success_url = reverse_lazy('patients')
    success_message = 'Patient successfully Added'

class AddMedcialRecordView(SuccessMessageMixin,CreateView):
    model = medical_record
    form_class = AddMedicalRecordForm
    template_name = 'patients/addmedicalrecord.html'
    success_url = reverse_lazy('patients')
    success_message = 'Patient successfully Added'

    def form_valid(self,form):
        patientidd = patient.objects.get(id=self.kwargs['pk'])
    
        form.instance.patientid = patientidd
        form.instance.userid = self.request.user #adding the logged in user to the frm instance
        return super().form_valid(form)



def assignurset(request,pk):
    patientobj = patient.objects.get(id=pk)
    assignednurse = User.objects.all()
    return render(request,'patients/assignurset.html',{
        'patientobj':patientobj,
        'assignednurse':assignednurse
        })


def AssignNurseView(request,pk):
    post = patient.objects.get(id=pk)
    #instance = request.POST['nurseid']
    r = User.objects.get(id=request.POST['nurseid'])
    if request.method == 'POST':       
        
        post.patient_assignednurse = r
        print(r)
        post.save()
        messages.success(request,f'Patient { post.patient_surname } { post.patient_name }has been Assinged to a Nurse')
        return redirect('patients')








