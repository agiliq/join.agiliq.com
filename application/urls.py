from django.conf.urls import patterns, include, url

urlpatterns = patterns('application.views',
    url(r'^authorize/$', 'oauth_authorize', name='oauth_authorize'),
    url(
      r'^app_authorize/$',
      'oauth_app_authorize',
      name='oauth_app_authorize'),
    url(r'^access_token/$', 'oauth_access_token', name='oauth_access_token'),
)
