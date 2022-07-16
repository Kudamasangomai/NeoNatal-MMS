from ast import Assign
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User 
# from django.utils import timezone
from datetime import datetime ,timedelta
from django.core.validators import  MaxValueValidator,MinValueValidator
from neonatal.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
# from django.urls import reverse
# User._meta.get_field('email').verbose_name = "new name"

class patient(models.Model):
    blood_type=(
        ("A"," A "),
        ("B","B"),
        ("C","C"),
    )
    patient_name = models.CharField(max_length=100)
    patient_surname = models.CharField(max_length=100,blank=True)
    patient_nid = models.CharField(max_length=20,default='',unique=True)
    patient_blood_type = models.CharField(max_length=10,choices = blood_type)  
    patient_condtion = models.CharField(max_length=100,default='')
    patient_assignednurse = models.ForeignKey(User,default=0,on_delete=models.CASCADE, db_constraint=False)


    def __str__(self):
        return self.patient_name

    
    def get_absolute_url(self):       
        return reverse('patient-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        r = User.objects.get(id=self.patient_assignednurse.id)
        if r: 
                            
            subject = "New patient - Neo Natal"   
            message = " A new Patient has been assigned to you."	
            recipient_list = [r.email,]
            send_mail(subject,message,EMAIL_HOST_USER,recipient_list,fail_silently = False)
            print(r.email)
            return super().save(*args, **kwargs)

class medical_record(models.Model):
    hiv_status=(
        ("Negative","Negative "),
        ("Positive","Posetive"),
  
    )
    drug_use=(
        ("Yes","Yes"),
        ("No","No"),
  
    )
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    patientid = models.ForeignKey(patient,on_delete = models.CASCADE)
    bptop= models.IntegerField(default='',validators=[MaxValueValidator(160),MinValueValidator(90)])
    bpbottom= models.IntegerField(default='',validators=[MaxValueValidator(100),MinValueValidator(50)])
    hbc = models.IntegerField(default='',validators=[MaxValueValidator(18),MinValueValidator(1)])#hemoglobin count
    usedrugs = models.CharField(max_length=100,choices=drug_use)
    hiv = models.CharField(max_length=100,choices = hiv_status)
    weight = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0)])
    height = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0)])
    bmi = models.DecimalField(max_digits=5,default='',decimal_places=2)


    def __str__(self):
        return self.patientid.patient_name

    def get_absolute_url(self):
        return reverse('patient-detail',kwargs={'pk':self.pk})




