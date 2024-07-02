from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import UnConferenceEvent, ScheduleTime, Room, Session


def serialize_one(entity, fields):
    return {
        field: print(field) or getattr(entity, field)
        for field in fields
    }


def serialize(entities, fields):
    return [
        {
            field: getattr(entity, field)
            for field in fields
        }
        for entity in entities
    ]


def event(request, event_id):
    event = get_object_or_404(UnConferenceEvent, id=event_id)
    times = ScheduleTime.objects.filter(unconference_event_id=event)
    rooms = Room.objects.filter(unconference_event_id=event)
    sessions = Session.objects.filter(room__in=rooms)
    return JsonResponse({
        'event': serialize_one(event, ['title', 'start', 'end', 'active']),
        'times': serialize(times, ['title', 'start', 'end', 'allow_sessions']),
        'rooms': serialize(rooms, ['title', 'capacity', 'description']),
        'sessions': serialize(
            sessions,
            ['leaders', 'schedule_time_id', 'room_id', 'title', 'description', 'type']
        )
    })


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
            ).select_related('room')
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
                "id": time.id,
                "title": time.title,
                "start": time.start,
                "sessions": sessions.filter(schedule_time=time),
            } for time in schedule_times]

            context["sessions"] = sessions
            context["schedule"] = schedule
        else:
            context["events"] = unconference_event

        return context

