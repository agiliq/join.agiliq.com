from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'registration.views.register',
        {'backend': 'user_profile.backends.RegistrationBackend'},
        name='registration_register'),
    url(r'^profile/$', 'user_profile.views.profile_home',
        name='user_profile_home'),
    url(r'^update_redirect_url/$', 'user_profile.views.update_redirect_url',
        name='update_redirect_url'),
)
