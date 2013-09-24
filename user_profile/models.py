from django.db import models
from utils.models import BaseAppModel
from django.contrib.auth.models import User


class UserProfile(BaseAppModel):
    user = models.OneToOneField(User)
    projects_url = models.URLField(null=True)
    code_url = models.URLField(null=True)

    def __unicode__(self):
        return self.user.email
