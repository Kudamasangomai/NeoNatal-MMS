
from random import random
from django.db import models
from twilio.rest import Client
from patients.models import patient
from datetime import datetime,timedelta
from django.contrib.auth.models import User 
from django.core.validators import  MaxValueValidator,MinValueValidator
import random


#Create your models here.https://medlineplus.gov/ency/article/003402.htm
#https://my.clevelandclinic.org/health/diseases/9685-stillbirth
#https://americanpregnancy.org/healthy-pregnancy/labor-and-birth/apgar-test/

def childregid():
     return str(random.randint( 100,9999))

class child(models.Model):
     score = [MaxValueValidator(2),MinValueValidator(0)]
     motherid = models.ForeignKey(patient,on_delete=models.CASCADE)
     childregno = models.IntegerField(default=childregid)
     heartrate = models.IntegerField(default='',validators =[MaxValueValidator(2),MinValueValidator(1)] )
     muscletone = models.IntegerField(default='',validators =score)
     skincolour = models.IntegerField(default='',validators =score)
     reflex = models.IntegerField(default='',validators =score)
     Breathing = models.IntegerField(default='',validators =score)
     agparscore = models.IntegerField(default=0,validators=[MaxValueValidator(10),MinValueValidator(0)])
     Dob = models.DateTimeField()
     nurseincharge = models.ForeignKey(User,on_delete=models.CASCADE)

     def __str__(self):
            return f'{ self.motherid.patient_name } child'
     
     #  #save method
     def save(self, *args, **kwargs):
        #if heartrate is less than 1 
        if self.heartrate < 2:
            #twilio code
            account_sid = 'AC786ed08d13a127ed6c6567f38533a55f'
            auth_token = 'eef515624c10273f2b57ed8718e81e81'
           # auth_token = '569149322e781ebd23f1c97d7d9936a0'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                           messaging_service_sid='MG43fefeae27269bdadf328bb970ede776',
                           body=f'New Born Child with regno  {self.childregno}. Has a heartrate of 1 Please monitor the baby',
                           from_='+19896834626',
                           to='+263777459622' 
                                    )

            print(message.sid)
     ##    return super().save(*args, **kwargs)

 


class childtest(models.Model):
     score = [MaxValueValidator(2),MinValueValidator(0)]
     child_regno = models.IntegerField(default='')
     heart_rate = models.IntegerField(default='',validators =[MaxValueValidator(2),MinValueValidator(1)] )
     muscle_tone = models.IntegerField(default='',validators =score)
     skin_colour = models.IntegerField(default='',validators =score)
     re_flex = models.IntegerField(default='',validators =score)
     Brea_thing = models.IntegerField(default='',validators =score)
     agpar_score = models.IntegerField(default=0,validators=[MaxValueValidator(10),MinValueValidator(0)])


     def __str__(self):
          return f'{self.child_regno}'
     
     #    #save method
     def save(self, *args, **kwargs):
        #if heartrate is less than 1 
        if self.heart_rate < 2:
            #twilio code
            account_sid = 'AC786ed08d13a127ed6c6567f38533a55f'
            auth_token = 'eef515624c10273f2b57ed8718e81e81'
           # auth_token = '569149322e781ebd23f1c97d7d9936a0'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                           messaging_service_sid='MG43fefeae27269bdadf328bb970ede776',
                           body=f'New Born Child with regno  {self.child_regno}. Has a heartrate of 1 Please monitor the baby',
                          from_='+19896834626',
                           to='+263777459622' 
                                    )

            print(message.sid)
        return super().save(*args, **kwargs)


# def deadchildid():
#      return str(random.randint( 11111,30253))
# class deadchild(models.Model):
#       motherid = models.ForeignKey(patient,on_delete=models.CASCADE)
#       deadchildregno = models.IntegerField(default=deadchildid)
     
    