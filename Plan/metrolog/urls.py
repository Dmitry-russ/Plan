from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (index, metrolog_create, metrolog_detail)


app_name = 'metrolog'
urlpatterns = [
    path('', index, name='index'),
    path('create/', metrolog_create, name='metrolog_create'),
    path('detail/<int:metrolog_id>/', metrolog_detail, name='metrolog_detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)