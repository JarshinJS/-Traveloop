from django import forms
from .models import Trip, TripStop, PackingItem, TripNote
from cities.models import City


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'description', 'start_date', 'end_date', 'cover_photo', 'total_budget', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. European Adventure 2025'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Describe your trip...'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'cover_photo': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'total_budget': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'checkbox-custom'}),
        }


class TripStopForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = TripStop
        fields = ['city', 'arrival_date', 'departure_date', 'notes']
        widgets = {
            'arrival_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Notes about this stop...'}),
        }


class PackingItemForm(forms.ModelForm):
    class Meta:
        model = PackingItem
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Item name'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


class TripNoteForm(forms.ModelForm):
    class Meta:
        model = TripNote
        fields = ['title', 'content', 'stop']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Note title'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Write your note...'}),
            'stop': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stop'].required = False
        self.fields['stop'].empty_label = '— General (no specific stop) —'
        if trip:
            self.fields['stop'].queryset = trip.stops.select_related('city').all()
        else:
            self.fields['stop'].queryset = TripStop.objects.none()
