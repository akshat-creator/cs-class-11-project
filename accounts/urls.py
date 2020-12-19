from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('customer_register/',views.customer_register.as_view(), name='customer_register'),
    path('shopkeeper_register/',views.shopkeeper_register.as_view(), name='shopkeeper_register'),
    path('login/',views.login_request, name='login'),
    path('logout/',views.logout_view, name='logout'),
]
