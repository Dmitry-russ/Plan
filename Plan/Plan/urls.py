from django.contrib import admin
from django.urls import include, path 

app_name = 'Plan'
urlpatterns = [
    path('', include('train.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]

handler404 = 'core.views.page_not_found'
handler403 = 'core.views.csrf_failure'
handler500 = 'core.views.internal_server_error'