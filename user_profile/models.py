from django.db import models
from django.contrib.auth.models import User

from utils.models import BaseAppModel


class UserProfile(BaseAppModel):
    user = models.OneToOneField(User)
    projects_url = models.URLField(null=True)
    code_url = models.URLField(null=True)

    def __unicode__(self):
        return self.user.email
