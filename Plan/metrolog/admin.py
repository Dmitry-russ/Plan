from django.contrib import admin

from .models import Measurement, Certificate, Manual


class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'type', 'dunumber',
        'description', 'location', 'model',
        'number', 'control_type', 'periodicity',
        'seral_number', 'date_control', 'date_end',
        'place', 'in_act', 'note',
        )
    search_fields = ('description', 'location', 'seral_number',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'metrolog', 'name',
        'file', 'default',
        )
    search_fields = ('metrolog', 'name', 'file',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class ManualAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'metrolog', 'name',
        'file', 'default',
        )
    search_fields = ('metrolog', 'name', 'file',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Manual, ManualAdmin)
