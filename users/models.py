from django.db import models
from django.db import models
from django.contrib.auth.models import User


class profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    image =  models.ImageField(default='default.jpg' ,upload_to = 'profile_pics')
    user_phone =  models.IntegerField()

    def __str__(self):
        return self.user.username
