from django.urls import include, path
from rest_framework import routers

from .views import (DoneMaiDateViewSet,
                    TrainViewSet,
                    CaseViewSet,
                    MaiNumViewSet,
                    MeasurementSet,
                    CertificateSet,
                    UserDataViewSet, )

v1_router = routers.DefaultRouter()
v1_router.register(r'train/mai/(?P<serial>[\w]+)/(?P<number>[\w]+)',
                   DoneMaiDateViewSet,
                   basename='mai')
v1_router.register(r'train/mai/(?P<info>[\w]+)',
                   DoneMaiDateViewSet,
                   basename='mai')
v1_router.register(r'train/maintenance/(?P<number>[\w]+)',
                   MaiNumViewSet,
                   basename='maintenance')
v1_router.register(r'train/case/(?P<serial>[\w]+)/(?P<number>[\w]+)',
                   CaseViewSet,
                   basename='case')
v1_router.register(r'train/listall',
                   TrainViewSet,
                   basename='alllist')
v1_router.register(r'train/list/(?P<number>[\w]+)',
                   TrainViewSet,
                   basename='list')
v1_router.register(r'metrolog/list',
                   MeasurementSet,
                   basename='list')
v1_router.register(r'certificate/list/(?P<id>[\w]+)',
                   CertificateSet,
                   basename='certificatelist')
v1_router.register(r'user/telegram/(?P<user>[\w]+)',
                   UserDataViewSet,
                   basename='telegramlist')

# v1_router.register(r'costs', CostViewSet, basename='costs')
# v1_router.register(r'groups', GroupViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('v1/certificate/list/<int:id>/', CertificateSet),
    # path('v1/metrolog/list/', MeasurementSet.as_view()),
]
