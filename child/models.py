from random import random
from django.db import models
from patients.models import patient
from datetime import datetime,timedelta
from django.contrib.auth.models import User 
from django.core.validators import  MaxValueValidator,MinValueValidator
import random

# Create your models here.https://medlineplus.gov/ency/article/003402.htm

def childregid():
     return str(random.randint( 100,9999))

class child(models.Model):
     score = [MaxValueValidator(2),MinValueValidator(0)]
     motherid = models.ForeignKey(patient,on_delete=models.CASCADE)
     childregno = models.IntegerField(default=childregid)
     heartrate = models.IntegerField(default='',validators =score )
     muscletone = models.IntegerField(default='',validators =score)
     skincolour = models.IntegerField(default='',validators =score)
     reflex = models.IntegerField(default='',validators =score)
     Breathing = models.IntegerField(default='',validators =score)
     agparscore = models.IntegerField(default=0,validators=[MaxValueValidator(10),MinValueValidator(0)])
     Dob = models.DateTimeField()
     nurseincharge = models.ForeignKey(User,on_delete=models.CASCADE)



     def __str__(self):
            return f'{ self.motherid.patient_name } child'


class childtest(models.Model):
     score = [MaxValueValidator(2),MinValueValidator(0)]
     child_regno = models.IntegerField(default='')
     heart_rate = models.IntegerField(default='',validators =score )
     muscle_tone = models.IntegerField(default='',validators =score)
     skin_colour = models.IntegerField(default='',validators =score)
     re_flex = models.IntegerField(default='',validators =score)
     Brea_thing = models.IntegerField(default='',validators =score)
     agpar_score = models.IntegerField(default=0,validators=[MaxValueValidator(10),MinValueValidator(0)])


     def __str__(self):
          return f'{self.child_regno}'
     
    