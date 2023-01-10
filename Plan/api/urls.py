from django.urls import path
from .views import index

urlpatterns = [
    # Главная страница
    path('', index),
] 