# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
]