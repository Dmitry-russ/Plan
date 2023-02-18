from django.contrib import admin
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordResetDoneView)
from django.urls import include, path

app_name = 'Plan'

user_patterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
]

urlpatterns = [
    path('', include('train.urls')),
    path('', include(user_patterns)),
    path('api/', include('api.urls')),
    path('auth/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]

handler404 = 'core.views.page_not_found'
handler403 = 'core.views.csrf_failure'
handler500 = 'core.views.internal_server_error'
