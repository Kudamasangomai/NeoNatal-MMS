from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from patients.models import *
from crispy_forms.layout import Layout, Fieldset, Submit



class AddUserForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

        def clean(self):
            email=self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("email exists")
            return self.cleaned_data

class  AddPatientForm(forms.ModelForm):
    

    class Meta:
        model = patient
        fields = '__all__'
        exclude = ['id']

class AddMedicalRecordForm(forms.ModelForm):

    bptop = forms.CharField(min_length=2,max_length=3)
    bpbottom = forms.CharField(min_length=2,max_length=3)
 
    class Meta:
        model = medical_record
        fields = '__all__'
        exclude = ['userid','patientid']


    