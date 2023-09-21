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
        label="Дата выдачи сертификата",
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'), )
    date_end = forms.DateField(
        label="Дата окончания действия сертификата",
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'),
        required=False,
    ),
    place = forms.CharField(
        # widget=forms.TextInput(attrs={'size': '90'}),
        label="Место расположения", )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label="Описание (название)", )
    note = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label="Примечание",
        required=False, )
    seral_number = forms.CharField(
        # widget=forms.TextInput(attrs={'size': '50'}),
        label="Сериный номер", required=False, )
    type = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label="Тип СИ", required=False, )
    organization = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label="Организация, проводящая метрологический контроль",
        required=False, )
    organization_fact = forms.CharField(
        widget=forms.TextInput(attrs={'size': '90'}),
        label="Организация, фактически проводившая метрологический контроль",
        required=False, )
    location = forms.ChoiceField(
        widget=forms.Select(attrs={'size': '1'}),
        choices=ALL_PLACE_CHOICES,
        label="Локация",
        required=True, )

    class Meta:
        model = Measurement
        fields = ('file', 'location',
                  'description', 'seral_number', 'date_control', 'date_end',
                  'place', 'periodicity', 'control_type', 'dunumber', 'model',
                  'date_control', 'number',
                  'in_act', 'organization',
                  'organization_fact', 'note', 'type',)


class NewCertificate(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('name', 'file',)
