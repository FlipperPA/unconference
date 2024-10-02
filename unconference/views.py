from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django.views.static import serve
import json
import os

from .models import UnConferenceEvent, ScheduleTime, Room, Session, UserEventData
from .decorators import ensure_guest_login

def serialize_one(entity, fields):
    return {
        field: getattr(entity, field)
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


@ensure_guest_login
def user_event_data(request, event_id):
    user_event_data, _new = UserEventData.objects.get_or_create(
        user=request.user,
        unconference_event_id=event_id,
    )
    if request.method == 'PUT':
        user_event_data.data = json.loads(request.body.decode("utf-8") or "{}")
        user_event_data.save()
    return JsonResponse({**user_event_data.data, 'id': user_event_data.id})


def swap_sessions(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Not allowed' }, status=403)
    data = json.loads(request.body.decode("utf-8") or "{}")
    session_1 = Session.objects.filter(id=data['session_1'].get('id')).first()
    session_2 = Session.objects.filter(id=data['session_2'].get('id')).first()

    if session_1 and session_2:
        session_1.room_id = None
        session_1.schedule_time_id = None
        session_1.save()

    if session_2:
        session_2.schedule_time_id = data['session_1']['time_id']
        session_2.room_id = data['session_1']['room_id']
        session_2.save()

    if session_1:
        session_1.schedule_time_id = data['session_2']['time_id']
        session_1.room_id = data['session_2']['room_id']
        session_1.save()

    return JsonResponse({})


def session(request, session_id):
    data = json.loads(request.body.decode("utf-8") or "{}")
    session = get_object_or_404(Session, id=session_id)
    allowed_user_ids = [u.id for u in session.users.all()]
    if not request.user.id in allowed_user_ids:
        return JsonResponse({'error': 'Not allowed' }, status=403)
    session.title = data['title']
    session.description = data['description']
    session.data['links'] = data['links']
    session.save()
    return JsonResponse({})


@ensure_guest_login
def user_json(request):
    fields = ['id', 'full_name', 'short_name', 'email', 'is_superuser', 'is_staff']
    return JsonResponse(serialize_one(request.user, fields))


def events(request):
    events = UnConferenceEvent.objects.filter(active=True)
    return JsonResponse({
        'events': serialize(events, ['id', 'title', 'start', 'end', 'active'])
    })

def event(request, event_id):
    event = get_object_or_404(UnConferenceEvent, id=event_id)
    location = event.location
    times = ScheduleTime.objects.filter(unconference_event_id=event)
    rooms = location.room_set.all()
    sessions = Session.objects.filter(unconference_event=event).prefetch_related('users')
    data = serialize_one(event, ['id', 'title', 'start', 'end', 'active'])
    data.update({
        'times': serialize(times, ['id', 'title', 'start', 'end', 'allow_sessions']),
        'rooms': serialize(rooms, ['id', 'title', 'capacity', 'description', 'geometry']),
        'location': location and serialize_one(location, ['id', 'title', 'geometry']),
        'sessions': serialize(
            sessions,
            ['id', 'leaders', 'schedule_time_id', 'room_id', 'title', 'description', 'type', 'leaders_info', 'data']
        )
    })
    return JsonResponse(data)


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
                location=unconference_event[0].location,
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


@ensure_csrf_cookie
def index(request, *args, **kwargs):
    path = kwargs.get('path', finders.find('index.html'))
    return serve(
        request,
        os.path.basename(path),
        os.path.dirname(path)
    )
    return response