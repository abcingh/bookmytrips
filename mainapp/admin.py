from django.contrib import admin
from .models import Tour, Profile, Cart, Country

# Register your models here.
admin.site.register(Tour)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Country)