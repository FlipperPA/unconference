from django.conf import settings
from django.db import models

from .settings import get_talk_choices


class UnConferenceEvent(models.Model):
    """
    Model to store unconference events.
    """

    title = models.TextField(null=False, blank=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    active = models.BooleanField(default=False)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "UnConference event"

    def __str__(self):
        return self.title


class Location(models.Model):
    """
    The building where a conference occurs
    """
    title = models.CharField(max_length=128)
    geometry = models.JSONField(default=dict)

    def __str__(self):
        return self.title


def default_data():
    return {
        'votes': {},
        'attendedance': {},
    }


class UserEventData(models.Model):
    """
    Model to store a users interactions (vodting, attendance, etc) with an event.
    The structure of the data column may vary from conference to conference.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unconference_event = models.ForeignKey(
        UnConferenceEvent,
        on_delete=models.PROTECT,
    )
    data = models.JSONField(default=default_data)


class ScheduleTime(models.Model):
    """
    Timeslots for the event's schedule; allow_sessions should be set to True for any
    timeslots where sessions can be schedule, and False for timeslots like lunch break.
    """

    unconference_event = models.ForeignKey(
        UnConferenceEvent,
        on_delete=models.PROTECT,
    )
    title = models.TextField(null=False, blank=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    allow_sessions = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["unconference_event", "title"], name="unique_schedule_time"
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.start:%H:%M %p} - {self.end:%H:%M %p})"


class Room(models.Model):
    """
    Rooms where sessions can take place.
    """
    title = models.TextField(null=False, blank=False)
    capacity = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    geometry = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.title}@{self.location}'


TALK_CHOICES = get_talk_choices()


class Session(models.Model):
    talk_choices = {}
    for t in get_talk_choices():
        talk_choices[t[0]] = t[1]

    leaders = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    schedule_time = models.ForeignKey(
        ScheduleTime,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        limit_choices_to={"allow_sessions": True},
    )
    room = models.ForeignKey(
        Room,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    session_type = models.PositiveSmallIntegerField(
        choices=get_talk_choices(),
        default=1,
        help_text="The type of session.",
    )
    data = models.JSONField(default=dict)
    unconference_event = models.ForeignKey(
        UnConferenceEvent,
        on_delete=models.PROTECT,
    )

    @property
    def leaders_info(self):
        return [
            {
                'id': user.id,
                'full_name': user.full_name,
            }
            for user in self.users.all()
        ]

    @property
    def type(self):
        return dict(TALK_CHOICES).get(self.session_type, 'UNKNOWN')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["schedule_time", "room"], name="unique_booking"
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.schedule_time})"
