from django.db import models
from django.conf import settings
from django.forms import ModelForm
from datetime import date
from django_resized import ResizedImageField


User = settings.AUTH_USER_MODEL
gender_choices = (('male', 'male'), ('female', 'female'))


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_image/user_{0}/{1}'.format(instance.user.id, filename)

DEFAULT = 'profile_image/default/default.png'

class Country(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=500, null=True, blank=True)
    country_description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.name}'


class Tour(models.Model):
    # country = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    tour_duration = models.CharField(max_length=100)
    title = models.TextField()
    image = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    amenities = models.TextField(null=True, blank=True)
    reasons_to_choose = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.country} {self.place}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.CharField(max_length=100)
    avatar = ResizedImageField( upload_to=user_directory_path, default=DEFAULT)
    dob = models.DateField()
    gender = models.CharField(choices=gender_choices, max_length=10)
    description = models.TextField()

    def __str__(self):
        return f'{self.user}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete = models.CASCADE)
    head_count = models.IntegerField(default = 0)
    tour_date = models.DateField()
    booking_date = models.DateField(("Date"), default=date.today)
    sell_status = models.BooleanField(default=False)
    total_cost = models.IntegerField(default=0)

    @property
    def total_amount(self):
        self.total_cost = self.head_count * self.tour.cost
        return self.total_cost

    

# import datetime

# class MyForm(forms.Form):
#     date = forms.DateField(...)

#     def clean_date(self):
#         date = self.cleaned_data['date']
#         if date < datetime.date.today():
#             raise forms.ValidationError("The date cannot be in the past!")
#         return date
