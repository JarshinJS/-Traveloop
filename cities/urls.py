from django.urls import path
from .views import city_search_view, city_detail_view, add_to_trip_view

app_name = 'cities'

urlpatterns = [
    path('', city_search_view, name='city_index'),
    path('search/', city_search_view, name='city_search'),
    path('<int:pk>/', city_detail_view, name='city_detail'),
    path('<int:pk>/add-to-trip/', add_to_trip_view, name='add_to_trip'),
]
