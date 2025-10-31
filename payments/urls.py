from django.urls import path
from . import views

urlpatterns = [
    path('', views.set_amount_view, name='set_amount'), 
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.payment_success_view, name='success'),
    path('cancel/', views.payment_cancel_view, name='cancel'),
]