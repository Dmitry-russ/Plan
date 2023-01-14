from django.contrib import admin

from .models import Serial, Train, Cases


class SerialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'serial', 'slug', 'created')
    search_fields = ('serial',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'

class TrainAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'serial', 'number', 'created', 'mileage', 'mileage_date', 'day_mileage',)
    search_fields = ('number', 'serial',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'

class CasesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'train', 'name', 'text', 'created')
    search_fields = ('name', 'train',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Serial, SerialAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Cases, CasesAdmin)