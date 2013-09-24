from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('user_profile.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^oauth/', include('application.urls')),
    url(r'^api/', include('api.urls')),
    url('^pages/', include('django.contrib.flatpages.urls')),

)
