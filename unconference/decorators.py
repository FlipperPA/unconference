from django.contrib.auth import get_user_model, login
import random, functools


def ensure_guest_login(func):
  @functools.wraps(func)
  def wrapped(request, *args, **kwargs):
    if not request.user.is_authenticated:
        User = get_user_model()
        email = f'guest+{random.random()}@example.com'
        user = User.objects.create(email=email)
        backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=backend)
    return func(request, *args, **kwargs)
  return wrapped
