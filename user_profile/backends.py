from __future__ import absolute_import

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, check_password
from registration.backends.default import DefaultBackend
from .forms import RegistrationForm
from user_profile.models import UserProfile


class EmailAuthBackend(ModelBackend):
    supports_inactive_user = False

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class RegistrationBackend(DefaultBackend):
    def get_form_class(self, request):
        return RegistrationForm

    def register(self, request, **kwargs):
        kwargs["username"] = kwargs["email"]
        user = super(RegistrationBackend, self).register(request, **kwargs)
        UserProfile.objects.create(user=user)
        return user
