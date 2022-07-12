from django.db import models
from patients.models import patient
from datetime import datetime,timedelta
from django.contrib.auth.models import User 
from django.core.validators import  MaxValueValidator,MinValueValidator

# Create your models here.https://medlineplus.gov/ency/article/003402.htm

class child(models.Model):
     score = [MaxValueValidator(2),MinValueValidator(0)]
     motherid = models.ForeignKey(patient,on_delete=models.CASCADE)
     heartrate = models.IntegerField(default='',validators =score )
     muscletone = models.IntegerField(default='',validators =score)
     skincolour = models.IntegerField(default='',validators =score)
     reflex = models.IntegerField(default='',validators =score)
     Breathing = models.IntegerField(default='',validators =score)
     Dob = models.DateTimeField()
     nurseincharge = models.ForeignKey(User,on_delete=models.CASCADE)



     def __str__(self):
            return f'{ self.motherid.patient_name } child'
