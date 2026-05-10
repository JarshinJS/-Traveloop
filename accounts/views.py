from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from .forms import SignupForm, ProfileUpdateForm
from .models import UserProfile

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('trip_list')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to Traveloop, {user.username}!')
            return redirect('trip_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'delete_account' in request.POST:
            return account_delete_view(request)

        post_data = request.POST.copy()
        post_data.setdefault('first_name', request.user.first_name)
        post_data.setdefault('last_name', request.user.last_name)
        post_data.setdefault('email', request.user.email)
        post_data.setdefault('language_preference', profile.language_preference or 'en')

        form = ProfileUpdateForm(post_data, request.FILES, instance=profile)
        if form.is_valid():
            # Update User fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


@login_required
@require_POST
def account_delete_view(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Your account has been deleted.')
    return redirect('dashboard')
