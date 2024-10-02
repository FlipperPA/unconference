from django.contrib import admin
from django.forms.widgets import TextInput
from django.db.models import TextField

from .models import UnConferenceEvent, ScheduleTime, Room, Session, UserEventData


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
    list_display = ("title", "capacity", "location")
    search_fields = ("title",)
    ordering = ("title", "location")
    fields = ("title", "capacity", "description", "location")
    list_filter = ("location",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "leaders", "schedule_time", "room")
    search_fields = ("title", "description")
    ordering = ("schedule_time", "room")
    fields = ("schedule_time", "room", "leaders", "title", "description", "session_type", "users")
    filter_horizontal = ('users',)
    list_filter = ("schedule_time__unconference_event", "session_type")
    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'users':

            return db_field.remote_field.model._default_manager.exclude(
                email__endswith="example.com",
            )

        super().get_field_queryset(db, db_field, request)


@admin.register(UserEventData)
class UserEventDataAdmin(admin.ModelAdmin):
    """
    Readonly admin for UserEventData
    """
    list_display = ("user", "unconference_event")
    readonly_fields = ("user", "unconference_event", "data")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False