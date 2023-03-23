from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='thebot-home'),
    path('chatarea', views.chatarea, name='thebot-chatarea'),
    path('about', views.about, name='thebot-about'),
]