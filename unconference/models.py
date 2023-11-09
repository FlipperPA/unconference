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

    class Meta:
        verbose_name = "UnConference event"

    def __str__(self):
        return f"{self.title}"


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
    max_sessions = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.start} - {self.end})"


class Room(models.Model):
    """
    Rooms where sessions can take place.
    """

    unconference_event = models.ForeignKey(
        UnConferenceEvent,
        on_delete=models.PROTECT,
    )
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Session(models.Model):
    leaders = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False)
    schedule_time = models.ForeignKey(
        ScheduleTime,
        on_delete=models.PROTECT,
        limit_choices_to={"allow_sessions": True},
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
    )
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    session_type = models.PositiveSmallIntegerField(
        choices=get_talk_choices(),
        default=1,
        help_text="The type of session.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["schedule_time", "room"], name="unique_booking"
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.schedule_time})"
