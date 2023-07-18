from django.urls import path

from .views import (metrolog_create, metrolog_detail,
                    metrolog_small_report, mai_export,
                    certificate_create, certificate_delete,
                    certificate_default)

app_name = 'metrolog'
urlpatterns = [
    path('', metrolog_small_report, name='metrolog_small_report'),
    path('create/', metrolog_create, name='metrolog_create'),
    path('detail/<int:metrolog_id>/', metrolog_detail, name='metrolog_detail'),
    path('certificate/create/<int:metrolog_id>/',
         certificate_create,
         name='certificate_create'),
    path('certificate/delete/<int:certificate_id>/',
         certificate_delete,
         name='certificate_delete'),
    path('certificate/default/<int:certificate_id>/',
         certificate_default,
         name='certificate_default'),
    path('export/', mai_export, name='mai_export_si'),
]
