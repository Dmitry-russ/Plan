from datetime import date

from django import forms

from .models import Measurement


class NewMetrolog(forms.ModelForm):
    date_control = forms.DateField(
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'))
    date_end = forms.DateField(
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'))

    class Meta:
        model = Measurement
        fields = ('type', 'dunumber',
                  'description', 'location', 'model',
                  'number', 'control_type', 'periodicity',
                  'seral_number', 'date_control', 'date_end',
                  'place', 'in_act', 'note',)
