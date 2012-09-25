from django.shortcuts import render_to_response
from application.models import Application
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def profile_home(request):
    applications = Application.objects.filter(user_profile=request.user.get_profile())
    return render_to_response("user_profile/profile_home.html",
                              {"applications": applications},
                              context_instance=RequestContext(request))
