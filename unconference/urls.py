from django.urls import path, re_path

from . import views


urlpatterns = [
    path("table/", views.HomeView.as_view()),
    path("api/event/<int:event_id>/", views.event),
    path("api/session/<int:session_id>/", views.session),
    path("api/swap-sessions/", views.swap_sessions),
    path("api/event/", views.events),
    path("api/user-event-data/<int:event_id>/", views.user_event_data),
    path("api/user.json", views.user_json),
    path("", views.index),
    re_path("^(help|settings|vote|session|map)", views.index),
]
