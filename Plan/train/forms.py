from django import forms

from .models import Train, Cases, DoneMaiDate


class CasesForm(forms.ModelForm):
    class Meta:
        model = Cases
        fields = ('name', 'text',)


class NewTrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ('serial', 'number', 'renter',
                  'mileage', 'mileage_date', 'day_mileage',)


class NewMaiForm(forms.ModelForm):
    class Meta:
        model = DoneMaiDate
        fields = ('maintenance', 'maintenance_date',
                  'mileage', 'place', 'comment',)
