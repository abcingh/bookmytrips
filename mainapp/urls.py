from django.urls import path
from mainapp import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
]