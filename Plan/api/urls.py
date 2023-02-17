from django.urls import include, path
from rest_framework import routers

from .views import DoneMaiDateViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'train/mai/(?P<number>[\w]+)',
                   DoneMaiDateViewSet,
                   basename='mai')
# v1_router.register(r'costs', CostViewSet, basename='costs')
# v1_router.register(r'groups', GroupViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
