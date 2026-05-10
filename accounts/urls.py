from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import signup_view, CustomLoginView, profile_view, account_delete_view

app_name = 'accounts'

urlpatterns = [
    path('register/', signup_view, name='register'),
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('delete/', account_delete_view, name='account_delete'),
]
