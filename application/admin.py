from django.contrib import admin

from application.models import Application, AuthorizationCode, AccessToken


admin.site.register(Application)
admin.site.register(AuthorizationCode)
admin.site.register(AccessToken)
