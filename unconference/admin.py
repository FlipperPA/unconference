from django.contrib import admin

from .models import UnConferenceEvent, ScheduleTime, Room, Session


@admin.register(UnConferenceEvent)
class UnConferenceEventAdmin(admin.ModelAdmin):
    list_display = ("title", "start", "end", "active")
    search_fields = ("title",)
    ordering = ("-active", "-start")
    fields = ("title", "start", "end", "active")
    list_filter = ("active",)


@admin.register(ScheduleTime)
class ScheduleTimeAdmin(admin.ModelAdmin):
    list_display = ("unconference_event", "title", "start", "end", "allow_sessions")
    search_fields = ("unconference_event", "title")
    ordering = ("unconference_event", "title")
    fields = ("unconference_event", "title", "start", "end", "allow_sessions")
    list_filter = ("unconference_event", "allow_sessions")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("unconference_event", "title")
    search_fields = ("unconference_event", "title")
    ordering = ("unconference_event", "title")
    fields = ("unconference_event", "title", "description")
    list_filter = ("unconference_event",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("schedule_time", "room", "title")
    search_fields = ("title", "description")
    ordering = ("schedule_time", "room")
    fields = ("schedule_time", "room", "title", "description", "session_type")
    list_filter = ("schedule_time__unconference_event", "session_type")
