from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import (train_list, cases_list, case_detail,
                    case_create, train_create, case_delete,
                    mai_list, mai_create, mai_detail, mai_create_from_list,
                    mai_delete, train_detail, mai_not_delete, mai_export,
                    train_small_report, )

app_name = 'train'
urlpatterns = [
    path('', train_list, name='train_list'),
    path('train/create/', train_create, name='train_create'),
    path('train/detail/<int:train_id>/', train_detail, name='train_detail'),
    path('train/smallreport/', train_small_report, name='train_small_report'),
    path('train/cases/<int:train_id>/', cases_list, name='cases_list'),
    path('train/case/<int:case_id>/', case_detail, name='case_detail'),
    path('train/case/create/<int:train_id>/', case_create, name='case_create'),
    path('train/case/delete/<int:case_id>/<int:train_id>/',
         case_delete, name='case_delete'),
    path('train/mai/<int:train_id>/', mai_list, name='mai_list'),
    path('train/mai/create/<int:train_id>/', mai_create, name='mai_create'),
    path('train/mai/delete/<int:mai_id>/', mai_delete, name='mai_delete'),
    path('train/mai/notdelete/<int:mai_id>/',
         mai_not_delete,
         name='mai_not_delete'),
    path('train/mai/create/<int:train_id>/<int:mai_id>/',
         mai_create_from_list,
         name='mai_create_from_list'),
    path('train/mai/detail/<int:mai_id>/', mai_detail, name='mai_detail'),
    path('train/mai/export/<int:train_id>/', mai_export, name='mai_export'),
    path('train/mai/export/all/', mai_export, name='mai_export_all'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
