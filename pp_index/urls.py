from django.urls import path
from .views import aboutus, CheckoutView, ppcards, HomeView, add_to_cart, ProductView, remove_from_cart
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('aboutus/', aboutus, name='aboutus'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('ppcards/', ppcards, name='ppcards'),
    path('product/<slug>/', ProductView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart')
    
]