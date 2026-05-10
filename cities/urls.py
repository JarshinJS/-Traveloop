from django.urls import path
from .views import city_search_view, city_detail_view

urlpatterns = [
    path('search/', city_search_view, name='city_search'),
    path('<int:pk>/', city_detail_view, name='city_detail'),
]
