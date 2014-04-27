from django.conf.urls import patterns, include, url

from registration.backends.default.views import RegistrationView


urlpatterns = patterns('',
    url(r'^register/$', RegistrationView.as_view(),
        {'backend': 'user_profile.backends.RegistrationBackend'},
        name='registration_register'),
    url(r'^login/$', 'user_profile.views.login',
        name='auth_login'),
    url(r'^profile/$', 'user_profile.views.profile_home',
        name='user_profile_home'),
    url(r'^update_redirect_url/$', 'user_profile.views.update_redirect_url',
        name='update_redirect_url'),
)
