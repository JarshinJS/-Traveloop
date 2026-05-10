from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard_home'),
    path('trips/', views.trip_list_view, name='trip_list'),
    path('trips/create/', views.trip_create_view, name='trip_create'),
    path('trips/new/', views.trip_create_view, name='trip_create'),
    path('trips/<int:pk>/', views.trip_detail_view, name='trip_detail'),
    path('trips/<int:pk>/edit/', views.trip_edit_view, name='trip_edit'),
    path('trips/<int:pk>/delete/', views.trip_delete_view, name='trip_delete'),
    path('trips/<int:pk>/build/', views.itinerary_builder_view, name='itinerary_builder'),
    path('trips/<int:pk>/view/', views.itinerary_view_view, name='itinerary_view'),
    path('trips/<int:pk>/budget/', views.budget_view, name='trip_budget'),
    path('trips/<int:pk>/packing/', views.packing_checklist_view, name='packing_checklist'),
    path('trips/<int:pk>/notes/', views.notes_view, name='trip_notes'),
    # AJAX endpoints
    path('trips/<int:pk>/stops/add/', views.add_stop_view, name='add_stop'),
    path('trips/<int:pk>/stops/<int:stop_id>/delete/', views.remove_stop_view, name='remove_stop'),
    path('stops/<int:stop_id>/remove/', views.remove_stop_view, name='remove_stop'),
    path('stops/<int:stop_id>/activities/add/', views.add_activity_view, name='add_activity'),
    path('trip-activities/<int:ta_id>/remove/', views.remove_activity_view, name='remove_activity'),
    path('trips/<int:pk>/packing/reset/', views.reset_packing_view, name='reset_packing'),
    path('packing/<int:item_id>/toggle/', views.toggle_packed_view, name='toggle_packed'),
    path('notes/<int:note_id>/edit/', views.note_edit_view, name='note_edit'),
    path('notes/<int:note_id>/delete/', views.note_delete_view, name='note_delete'),
    # Reorder
    path('trips/<int:pk>/stops/reorder/', views.reorder_stops_view, name='reorder_stops'),
    # Public share
    path('trips/share/<uuid:token>/', views.public_itinerary_view, name='public_itinerary'),
    path('trips/share/<uuid:token>/clone/', views.copy_trip_view, name='copy_trip'),
    path('share/<uuid:token>/', views.public_itinerary_view, name='public_itinerary'),
    path('share/<uuid:token>/copy/', views.copy_trip_view, name='copy_trip'),
]
