from datetime import date

from django import forms
from train.models import ALL_PLACE_CHOICES

from .models import Measurement, Certificate


class FilterForm(forms.Form):
    location = forms.ChoiceField(label='Локация',
                                 required=False,
                                 choices=[('', ''), ] + ALL_PLACE_CHOICES,
                                 )

    place = forms.CharField(label='Расположение',
                            required=False, )
    seral_number = forms.CharField(label='Серийный номер',
                                   required=False, )
    description = forms.CharField(label='Наименование (описание) СИ',
                                  required=False, )


class NewMetrolog(forms.ModelForm):
    date_control = forms.DateField(
        label="Дата проверки",
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'), )
    date_end = forms.DateField(
        label="Дата окончания проверки",
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'))
    place = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 10, 'rows': 1}),
        label="Место расположения", )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        label="Описание", )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        label="Примечание",
        required=False, )
    seral_number = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 20, 'rows': 1}),
        label="Сериный номер", required=False, )

    class Meta:
        model = Measurement
        fields = ('type', 'dunumber',
                  'description', 'location', 'model',
                  'number', 'control_type', 'periodicity', 'organization',
                  'organization_fact',
                  'seral_number', 'date_control', 'date_end',
                  'place', 'in_act', 'note',)


class NewCertificate(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('name', 'file',)
