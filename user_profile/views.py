from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login as auth_login

from application.models import Application
from user_profile.forms import RedirectForm, AuthenticationForm


@login_required
def profile_home(request):
    application = Application.objects.get(
        user_profile=request.user.get_profile())
    initial_dict = {"redirect_uri": application.redirect_uri}
    return render_to_response("user_profile/profile_home.html",
                              {"application": application,
                               "form": RedirectForm(initial=initial_dict)},
                              context_instance=RequestContext(request))


@login_required
@require_POST
def update_redirect_url(request):
    form = RedirectForm(request.POST)
    application = Application.objects.get(
               user_profile=request.user.get_profile())
    initial_dict = {"redirect_uri": application.redirect_uri}
    if form.is_valid():
        application.redirect_uri = form.cleaned_data["redirect_uri"]
        application.save()
        return HttpResponseRedirect(reverse("user_profile_home"))
    return render_to_response("user_profile/profile_home.html",
                              {"application": application,
                               "form": RedirectForm(initial=initial_dict)},
                              context_instance=RequestContext(request))


def login(request):
    return auth_login(request, authentication_form=AuthenticationForm)
