from django import forms

from .models import BudgetEntry


class BudgetEntryForm(forms.ModelForm):
    class Meta:
        model = BudgetEntry
        fields = ['stop', 'category', 'description', 'amount']
        widgets = {
            'stop': forms.Select(attrs={'class': 'form-select bg-body-tertiary'}),
            'category': forms.Select(attrs={'class': 'form-select bg-body-tertiary'}),
            'description': forms.TextInput(attrs={
                'class': 'form-control bg-body-tertiary',
                'placeholder': 'e.g. Train tickets',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control bg-body-tertiary',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
        }

    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stop'].required = False
        self.fields['stop'].empty_label = 'General trip cost'
        if trip:
            self.fields['stop'].queryset = trip.stops.select_related('city').all()
        else:
            self.fields['stop'].queryset = self.fields['stop'].queryset.none()

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("Amount cannot be negative.")
        return amount
