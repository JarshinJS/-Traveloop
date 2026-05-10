from django.urls import path
from .views import activity_search_view, activity_detail_view

app_name = 'activities'

urlpatterns = [
    path('', activity_search_view, name='activity_index'),
    path('search/', activity_search_view, name='activity_search'),
    path('<int:pk>/', activity_detail_view, name='activity_detail'),
]
