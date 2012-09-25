from django.db import models
from user_profile.models import UserProfile
from utils.models import BaseAppModel
from django.db.models.signals import post_save
from django.core.mail import mail_admins
from django.template.loader import render_to_string

class Resume(BaseAppModel):
    user_profile = models.ForeignKey(UserProfile)
    resume = models.FileField(upload_to="resumes")

    def __unicode__(self):
        return "Resume: %s" % self.user_profile

def send_mail_to_admin(sender, **kwargs):
    user = kwargs["instance"].user_profile.user
    subject = "%s has applied for a job through the API" % user.get_full_name()
    message = render_to_string("api/application_message.txt",
                               {"resume": kwargs["instance"]})
    mail_admins(subject, message)

post_save.connect(send_mail_to_admin, sender=Resume)
