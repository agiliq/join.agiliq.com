from django.http import HttpResponseRedirect
from application.models import AccessToken
import urllib

def verify_access_token(fn):
    def inner(request, **kwargs):
        access_token = request.GET.get("access_token")
        if not access_token:
            redirect_url = request.META.get("REFERER", "/")
            params = {"error": "invalid_request",
                      "error_description": "Missing Access Token"}
            redirect_url += "?%s" % urllib.urlencode(params)
            return HttpResponseRedirect(redirect_url)
        try:
            access_token = AccessToken.objects.get(token=access_token)
        except AccessToken.DoesNotExist:
            redirect_url = request.META.get("REFERER", "/")
            params = {"error": "invalid_request",
                      "error_description": "Invalid access token"}
            redirect_url += "?%s" % urllib.urlencode(params)
            return HttpResponseRedirect(redirect_url)
        kwargs["access_token"] = access_token
        return fn(request, **kwargs)
    return inner
