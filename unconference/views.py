from django.shortcuts import render
from django.views.generic import TemplateView

from .models import UnConferenceEvent, ScheduleTime, Room, Session


class HomeView(TemplateView):
    template_name = "unconference/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get("uid", None):
            unconference_event = UnConferenceEvent.objects.filter(
                id=self.request.GET["uid"],
            )
        else:
            unconference_event = UnConferenceEvent.objects.filter(active=True)

        if unconference_event.count() == 1:
            self.template_name = "unconference/schedule.html"
            context["event"] = unconference_event[0]

            schedule = {}
            schedule_times = ScheduleTime.objects.filter(
                unconference_event=context["event"],
            ).order_by(
                "start",
            )
            rooms = Room.objects.filter(
                unconference_event=context["event"],
            ).order_by(
                "title",
            )
            sessions = Session.objects.filter(
                schedule_time__unconference_event=context["event"],
                schedule_time__isnull=False,
                room__isnull=False,
            )
            schedule = {
                r.title: {
                    s.title: {} for s in schedule_times
                } for r in rooms
            }
            for s in sessions:
                schedule[s.room.title][s.schedule_time.title] = {
                    "id": s.id,
                    "leaders": s.leaders,
                    "title": s.title,
                    "description": s.description,
                    "session_type": Session.talk_choices[s.session_type],
                }
            context["schedule_times"] = [{
                "title": s.title,
                "start": s.start,
            } for s in schedule_times]
            context["sessions"] = sessions
            context["schedule"] = schedule
        else:
            context["events"] = unconference_event

        return context

