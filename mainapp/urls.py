from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('countries/<str:name>/', views.tour_select, name='tourselect'),
    path('', views.index, name = 'index'),
    path('profile', views.profile, name = 'profile'),
    path('profile/update/', views.update_profile, name = 'update'),
    path('tour_id/<int:tour_id>', views.select_tour, name = 'select_tour'),
    path('add_to_cart/<int:tour_id>', views.add_to_cart, name = 'add_to_cart'),
    path('checkout/<int:cart_id>', views.checkout, name = 'checkout'),
    path('handlerequest', views.handlerequest, name = 'handlerequest')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+= (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))