from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'^resume/upload/$', 'resume_upload', name='resume_upload'),
)
