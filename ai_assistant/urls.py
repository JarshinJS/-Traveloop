from django.urls import path
from . import views

app_name = "ai_assistant"

urlpatterns = [
    path("chat/", views.chat_api, name="chat"),
    path("suggestions/<int:trip_id>/", views.smart_suggestions_api, name="suggestions"),
]
