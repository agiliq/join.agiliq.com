from __future__ import absolute_import

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, check_password
# from django.contrib.sites.models import Site
# from django.contrib.sites.models import RequestSite

from registration.backends.default.views import RegistrationView
# from registration.models import RegistrationProfile
# from registration.views import RegistrationView
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


class RegistrationBackend(RegistrationView):
    def get_form_class(self, request):
        return RegistrationForm

    def register(self, request, **kwargs):
        kwargs["username"] = kwargs["email"]
        user = super(RegistrationBackend, self).register(request, **kwargs)
        UserProfile.objects.create(user=user)
        return user
    
