from django.contrib import admin
from django.forms.widgets import TextInput
from django.db.models import TextField

from .models import UnConferenceEvent, ScheduleTime, Room, Session


class TextInputModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': TextInput},
    }


@admin.register(UnConferenceEvent)
class UnConferenceEventAdmin(TextInputModelAdmin):
    list_display = ("title", "start", "end", "active")
    search_fields = ("title",)
    ordering = ("-active", "-start")
    fields = ("title", "start", "end", "active")
    list_filter = ("active",)


@admin.register(ScheduleTime)
class ScheduleTimeAdmin(TextInputModelAdmin):
    list_display = ("title", "start", "end", "allow_sessions", "unconference_event")
    search_fields = ("title", "unconference_event")
    ordering = ("title", "unconference_event")
    fields = ("title", "start", "end", "allow_sessions", "unconference_event")
    list_filter = ("allow_sessions", "unconference_event")


@admin.register(Room)
class RoomAdmin(TextInputModelAdmin):
    list_display = ("title", "unconference_event")
    search_fields = ("title", "unconference_event")
    ordering = ("title", "unconference_event")
    fields = ("title", "description", "unconference_event")
    list_filter = ("unconference_event",)


@admin.register(Session)
class SessionAdmin(TextInputModelAdmin):
    list_display = ("schedule_time", "room", "title")
    search_fields = ("title", "description")
    ordering = ("schedule_time", "room")
    fields = ("leaders", "schedule_time", "room", "title", "description", "session_type")
    list_filter = ("schedule_time__unconference_event", "session_type")
