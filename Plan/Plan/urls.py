from django.contrib import admin
from django.urls import include, path 

app_name = 'Plan'
urlpatterns = [
    path('', index, name='index'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]