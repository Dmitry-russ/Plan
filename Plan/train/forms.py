from datetime import date

from django import forms

from .models import Train, Cases, DoneMaiDate


class CasesForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Cases
        fields = ('name', 'text', 'file',)


class NewTrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ('serial', 'number', 'renter',
                  'mileage', 'mileage_date', 'day_mileage',)


class NewMaiForm(forms.ModelForm):
    maintenance_date = forms.DateField(
        label='Дата',
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'))

    class Meta:
        model = DoneMaiDate
        fields = ('maintenance', 'maintenance_date',
                  'mileage', 'place', 'comment',)


class NewMaiFormFromList(forms.ModelForm):
    maintenance_date = forms.DateField(
        label='Дата',
        required=True,
        input_formats=['%d.%m.%Y'],
        initial=format(date.today(), '%d.%m.%Y'))

    class Meta:
        model = DoneMaiDate

        fields = ('maintenance_date',
                  'mileage', 'place', 'comment',)
