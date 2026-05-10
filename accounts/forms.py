from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': ' ',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': ' ',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': ' ',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': ' ',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': ' ',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': ' ',
        })


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': ' '}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': ' '}),
        }


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('ja', 'Japanese'),
        ('zh', 'Chinese'),
        ('hi', 'Hindi'),
        ('ar', 'Arabic'),
    ]

    language_preference = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'input-field'}),
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'language_preference']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', False)
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (max 2 MB).")
            content_type = getattr(avatar, 'content_type', '')
            if content_type and not content_type.startswith('image/'):
                raise forms.ValidationError("Avatar must be an image file.")
        return avatar
