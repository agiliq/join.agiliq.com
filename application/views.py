from django.http import HttpResponse, HttpResponseRedirect
from application.models import Application, AuthorizationCode, \
    CLIENT_PARAMS_SPACE, AccessToken
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import urllib
from application.forms import OAuthApplicationAuthorizationForm
from django.template import RequestContext
from django.shortcuts import render_to_response
import random
import json


def oauth_authorize(request):
    client_id = request.GET.get("client_id")
    if not client_id:
        redirect_url = "%s?%s" % (request.META.get("REFERER", "/"),
                                 urllib.urlencode(
                                  {"error": "invalid_client",
                                  "error_description": "Missing Client Id"}))
        return HttpResponseRedirect(redirect_url)
    try:
        application = Application.objects.get(client_id=client_id)
    except Application.DoesNotExist:
        redirect_url = "%s?%s" % (request.META.get("REFERER", "/"),
                                 urllib.urlencode(
                                 {"error": "invalid_client",
                                 "error_description": "Invalid Client Id"}))
        return HttpResponseRedirect(redirect_url)
    redirect_uri = request.GET.get("redirect_uri")
    if not redirect_uri:
        redirect_url = "%s?%s" % (
                             application.redirect_uri,
                             urllib.urlencode(
                              {"error": "invalid_request",
                              "error_description": "Missing Redirect URI"}))
        return HttpResponseRedirect(redirect_url)
    if not application.redirect_uri == redirect_uri:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                           urllib.urlencode(
                           {"error": "invalid_request",
                           "error_description": "Redirect" + \
                               " URI does not match"}))
        return HttpResponseRedirect(redirect_url)
    params = request.GET.copy()
    params.update({"client_id": application.client_id,
                   "redirect_uri": application.redirect_uri})
    return HttpResponseRedirect("%s?%s" % (reverse("oauth_app_authorize"),
                                          urllib.urlencode(params)))


def generate_token():
    return "".join(
         [random.choice(CLIENT_PARAMS_SPACE) for ii in range(0, 50)])


@login_required
def oauth_app_authorize(request):
    if request.method == "POST":
        form = OAuthApplicationAuthorizationForm(request.POST)
        if form.is_valid():
            try:
                application = Application.objects.get(
                                client_id=form.cleaned_data["client_id"])
            except Application.DoesNotExist:
                redirect_url = "%s?%s" % (request.META.get("REFERER", "/"),
                                         urllib.urlencode(
                                         {"error": "invalid_client",
                                         "error_" + \
                                         "description": "Invalid Client Id"}))
                return HttpResponseRedirect(redirect_url)
            if request.POST.get("authorized") == "Reject":
                return HttpResponseRedirect(
                          "%s?%s" % (
                                 application.redirect_uri,
                                 urllib.urlencode({"error": "access_denied",
                                 "error_description": "User" + \
                                  "has rejected the authorization"})))
            if application.redirect_uri != form.cleaned_data["redirect_uri"]:
                redirect_url = "%s?%s" % (application.redirect_uri or "",
                                          urllib.urlencode(
                                            {"error": "invalid_request",
                                            "error_description": "Redirect" + \
                                               "URI does not match"}))
                return HttpResponseRedirect(redirect_url)
            user_profile = request.user.get_profile()
            AuthorizationCode.objects.filter(
                             application=application,
                             user_profile=user_profile).delete()
            auth_code = AuthorizationCode.objects.create(
                                            application=application,
                                            user_profile=user_profile,
                                            token=generate_token())
            params = {"code": auth_code.token}
            if form.cleaned_data["state"]:
                params.update({"state": form.cleaned_data["state"]})
            return HttpResponseRedirect(
                 "%s?%s" % (application.redirect_uri,
                            urllib.urlencode(params)))
    else:
        params = request.GET.copy()
        form = OAuthApplicationAuthorizationForm(initial=params)
        try:
            application = Application.objects.get(
                          client_id=form.initial["client_id"])
        except Application.DoesNotExist:
            redirect_url = "%s?%s" % (request.META.get("REFERER", "/"),
                                      urllib.urlencode(
                                     {"error": "invalid_client",
                                     "error_" + \
                               "description": "Invalid Client Id"}))
            return HttpResponseRedirect(redirect_url)
    return render_to_response("application/authorize.html",
                              {"form": form,
                               "application": application},
                              context_instance=RequestContext(request))


def oauth_access_token(request):
    params = request.GET.copy()
    client_id = params.get("client_id")
    if not client_id:
        redirect_url = "%s?%s" % (request.META.get("REFERER", "/"),
                                 urllib.urlencode({"error": "invalid_request",
                                                   "error_" + \
                                  "description": "Missing Client Id"}))
        return HttpResponseRedirect(redirect_url)
    try:
        application = Application.objects.get(client_id=client_id)
    except Application.DoesNotExist:
        redirect_url = "%s?%s" % (request.META.get("REFERER", "/"),
                                 urllib.urlencode(
                                  {"error": "invalid_request",
                                  "error_description": "Invalid Client Id"}))
        return HttpResponseRedirect(redirect_url)
    redirect_uri = request.GET.get("redirect_uri")
    if not redirect_uri:
        redirect_url = "%s?%s" % (application.redirect_uri,
                                 urllib.urlencode(
                               {"error": "invalid_request",
                               "error_description": "Missing Redirect URI"}))
        return HttpResponseRedirect(redirect_url)
    if not application.redirect_uri == redirect_uri:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                        {"error": "invalid_request",
                        "error_description": "Redirect URI does not match"}))
        return HttpResponseRedirect(redirect_url)
    auth_code = params.get("code")
    if not auth_code:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                         {"error": "invalid_request",
                         "error_description": "Missing Authorization Code"}))
        return HttpResponseRedirect(redirect_url)
    try:
        authorization = AuthorizationCode.objects.get(token=auth_code)
    except AuthorizationCode.DoesNotExist:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                        {"error": "invalid_request",
                        "error_description": "Invalid Authorization Code"}))
        return HttpResponseRedirect(redirect_url)
    if authorization.application.client_id != client_id:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                         {"error": "invalid_request",
                         "error_description": "Invalid Authorization Code"}))
        return HttpResponseRedirect(redirect_url)
    if authorization.application.redirect_uri != redirect_uri:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                      {"error": "invalid_request",
                      "error_description": "Invalid Authorization Code"}))
        return HttpResponseRedirect(redirect_url)
    client_secret = params.get("client_secret")
    if not client_secret:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                      {"error": "invalid_request",
                      "error_description": "Missing Client Secret"}))
        return HttpResponseRedirect(redirect_url)
    if authorization.application.client_secret != client_secret:
        redirect_url = "%s?%s" % (application.redirect_uri or "",
                                 urllib.urlencode(
                          {"error": "invalid_request",
                          "error_description": "Invalid Client Secret"}))
        return HttpResponseRedirect(redirect_url)
    AccessToken.objects.filter(user_profile=authorization.user_profile,
                               application=authorization.application).delete()
    access_token = AccessToken.objects.create(
                          user_profile=authorization.user_profile,
                          application=authorization.application,
                          token=generate_token())
    access_params = {
       "access_token": access_token.token,
       "token_type": "simple",
     }
    return HttpResponse(
            json.dumps(access_params),
            content_type="application/json")
