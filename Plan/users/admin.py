from django.contrib import admin
from .models import UserData


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('author', 'telegram')
    search_fields = ('author',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(UserData, UserDataAdmin)
