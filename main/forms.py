from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from patients.models import *
from child.models import *
from datetime import datetime


class Dateinput(forms.DateInput):
    input_type= 'date'

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
        exclude = ['id','patient_date_added']

class AddMedicalRecordForm(forms.ModelForm):

    bptop = forms.CharField(min_length=2,max_length=3)
    bpbottom = forms.CharField(min_length=2,max_length=3)
 
    class Meta:
        model = medical_record
        fields = '__all__'
        exclude = ['userid','patientid']

class Addchildform(forms.ModelForm):
    heartrate  = forms.IntegerField(min_value = 0 , max_value= 2  )
    muscletone  = forms.IntegerField(min_value = 0 , max_value= 2  )
    skincolour = forms.IntegerField(min_value = 0 , max_value= 2  )
    reflex  = forms.IntegerField(min_value = 0 , max_value= 2  )
    Breathing = forms.IntegerField(min_value = 0 , max_value= 2  )


    class Meta:
        model = child
        fields = '__all__'
        exclude = ['motherid','nurseincharge','childregno']
        widgets = {'Dob':Dateinput()}
    




class Addchildtestform(forms.ModelForm):
    heart_rate  = forms.IntegerField(min_value = 0 , max_value= 2  )
    muscle_tone  = forms.IntegerField(min_value = 0 , max_value= 2  )
    skin_colour = forms.IntegerField(min_value = 0 , max_value= 2  )
    re_flex  = forms.IntegerField(min_value = 0 , max_value= 2  )
    Brea_thing = forms.IntegerField(min_value = 0 , max_value= 2  )


    class Meta:
        model = childtest
        fields = '__all__'
        exclude = ['child_regno']
        
   


    