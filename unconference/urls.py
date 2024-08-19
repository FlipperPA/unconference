from django.urls import path, re_path

from .views import index, event, user_event_data, user_json

urlpatterns = [
    path("api/event/<int:event_id>/", event),
    path("api/user-event-data/<int:event_id>/", user_event_data),
    path("api/user.json", user_json),
    path("", index),
    re_path("(help|settings|vote|session)", index),
]
