from redis import Redis
from rq import Queue

from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from utils.models import BaseAppModel
from user_profile.models import UserProfile

q = Queue(connection=Redis())


class Resume(BaseAppModel):
    user_profile = models.ForeignKey(UserProfile)
    resume = models.FileField(upload_to="resumes")

    def __unicode__(self):
        return "Resume: %s" % self.user_profile


def send_mail_to_admin(sender, **kwargs):
    user = kwargs["instance"].user_profile.user
    subject = "%s has applied for a job through the API" % user.get_full_name()
    message = render_to_string("api/application_message.txt",
                               {"resume": kwargs["instance"],
                                "site": Site.objects.get_current()})
    q.enqueue(send_mail, subject, message, settings.DEFAULT_FROM_EMAIL,
              settings.JOB_MANAGERS)


def send_mail_to_applicant(sender, **kwargs):
    user = kwargs["instance"].user_profile.user
    site = Site.objects.get_current()
    subject = "Thank you for applying to %s" % site.name
    message = render_to_string("api/application_confirmation.txt",
                               {"resume": kwargs["instance"],
                                "site": site})
    q.enqueue(send_mail, subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

post_save.connect(send_mail_to_admin, sender=Resume)
post_save.connect(send_mail_to_applicant, sender=Resume)
