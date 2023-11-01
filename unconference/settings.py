from django.conf import settings


def get_talk_choices():
    """
    A list of choice types.
    """

    return getattr(
        settings,
        "UNCONFERENCE_TALK_CHOICES",
        (
            (1, "Talk"),
            (2, "Discussion"),
            (3, "Hands-On"),
        )
    )
