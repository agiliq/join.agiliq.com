from django.db import models
from utils.models import BaseAppModel
from user_profile.models import UserProfile
from registration.signals import user_activated
import random

CLIENT_PARAMS_SPACE = "0123456789abcdefghijk" + \
                       "lmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Application(BaseAppModel):
    user_profile = models.ForeignKey(UserProfile)
    client_id = models.CharField(max_length=50)
    client_secret = models.CharField(max_length=50)
    redirect_uri = models.URLField(verify_exists=False, null=True)

    def __unicode__(self):
        return "%s : %s" % (self.user_profile.user.email, self.client_id)


class AuthorizationCode(BaseAppModel):
    application = models.ForeignKey(Application)
    user_profile = models.ForeignKey(UserProfile)
    token = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s : %s" % (self.application, self.token)


class AccessToken(BaseAppModel):
    user_profile = models.ForeignKey(UserProfile)
    application = models.ForeignKey(Application)
    token = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s : %s" % (self.user_profile, self.token)


def create_first_application(sender, **kwargs):
    user_profile = kwargs["user"].get_profile()
    if not Application.objects.filter(user_profile=user_profile).count():
        client_id = "".join([random.choice(CLIENT_PARAMS_SPACE) \
                                           for ii in range(0, 50)])
        client_secret = "".join([random.choice(CLIENT_PARAMS_SPACE) \
                                                    for ii in range(0, 50)])
        Application.objects.create(user_profile=user_profile,
                                   client_id=client_id,
                                   client_secret=client_secret)
user_activated.connect(create_first_application)
