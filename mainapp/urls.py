from django.urls import path
from mainapp import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update'),

]

