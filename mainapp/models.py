from django.db import models
from django.conf import settings
from django.forms import ModelForm



User = settings.AUTH_USER_MODEL
gender_choices = (('male', 'male'),
                ('female', 'female'))

class Tour(models.Model):
    country = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    tour_duration = models.IntegerField()
    title = models.TextField()
    image = models.CharField(max_length=100, null=True)
    description = models.TextField()
    cost = models.IntegerField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(choices=gender_choices, max_length=10)
    description = models.TextField()



