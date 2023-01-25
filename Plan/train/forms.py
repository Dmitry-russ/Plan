from django import forms

from .models import Train, Cases, Maintenance


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
        model = Maintenance
        fields = ('train', 'maintenance', 'maintenance_date',
                  'mileage', 'place', 'comment',)
