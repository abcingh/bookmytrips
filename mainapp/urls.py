from django.urls import path
from mainapp import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('countries/<str:name>/', views.tour_select, name='tourselect'),
    path('', views.index, name = 'index'),
    path('profile', views.profile, name = 'profile'),
    path('profile/update/', views.update_profile, name = 'update'),
    # path('something/<int:tour_id>', views.select_tour, name = 'select_tour'),
    # path('something/<int:tour_id>/add_to_cart/<int:tour_id>', views.add_to_cart, name = 'add_to_cart')

]

