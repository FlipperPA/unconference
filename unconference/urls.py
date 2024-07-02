from django.urls import path

from .views import HomeView, event

urlpatterns = [
    path("event/<int:event_id>", event),
    path("", HomeView.as_view()),
]
