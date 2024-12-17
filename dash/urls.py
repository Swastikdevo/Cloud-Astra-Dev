from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.members, name='members'),
    path('webhook/', views.webhook, name='webhook'),
    path('stats/', views.stats, name='stats'),
    path('ivr-response/', views.ivr_response, name='ivr-response'),
    # path('create_payment_link/', views.create_payment_link, name='create_payment_link'),
    path('process-input/', views.process_input, name='process-input'),

]

