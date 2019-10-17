from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL
gender_choices = (('male', 'male'),
                ('female', 'female'))

class Tour(models.Model):
    country = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    stay_duration = models.CharField(max_length=50)
    title = models.TextField()
    description = models.TextField()
    cost = models.IntegerField()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(choices=gender_choices, max_length=10)
    description = models.TextField()



