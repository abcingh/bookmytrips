from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    # path('search/', views.search, name='search'),
    path('countries/<int:id>/', views.tour_packages, name='tourselect'),
    path('profile/', views.profile, name = 'profile'),
    # path('profile/update/', views.update_profile, name = 'update'),
    path('tour-id/<int:tour_id>', views.select_tour, name = 'select_tour'),
    path('add-to-cart/<int:tour_id>', views.add_to_cart, name = 'add_to_cart'),
    path('cart-items/', views.cart_items, name = 'cart_items'),
    # path('checkout/<int:cart_id>', views.checkout, name = 'checkout'),
    path('handlerequest', views.handlerequest, name = 'handlerequest'),
    path('tour-detail/<int:order_id>', views.booked_tours_detail, name = 'booked_tours_detail')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+= (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
