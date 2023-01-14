from django import forms

from .models import Train, Cases


class CasesForm(forms.ModelForm):
    class Meta:
        model = Cases
        fields = ('name', 'text',)


class NewCaseForm(forms.ModelForm):
    class Meta:
        model = Cases
        fields = ('name', 'text',)


class NewTrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ('serial', 'number', 'renter',
                  'mileage', 'mileage_date', 'day_mileage',)

# class CasesForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text',)
