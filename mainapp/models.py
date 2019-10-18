from django.db import models
from django.conf import settings
from django.forms import ModelForm
from datetime import date

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
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete = models.CASCADE)
    head_count = models.IntegerField(default = 0)
    tour_date = models.DateField()
    booking_date = models.DateField(("Date"), default=date.today)
    sell_status = models.BooleanField(default=False)
    
    

    


# import datetime

# class MyForm(forms.Form):
#     date = forms.DateField(...)

#     def clean_date(self):
#         date = self.cleaned_data['date']
#         if date < datetime.date.today():
#             raise forms.ValidationError("The date cannot be in the past!")
#         return date