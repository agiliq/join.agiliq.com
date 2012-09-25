from utils.views import verify_access_token
from api.forms import ResumeUploadForm
from api.models import Resume
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
@verify_access_token
@require_POST
def resume_upload(request, access_token=None):
    form = ResumeUploadForm(request.POST, request.FILES)
    if form.is_valid():
        user_profile = access_token.user_profile
        user = user_profile.user
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.save()
        Resume.objects.filter(user_profile=user_profile).delete()
        Resume.objects.create(user_profile=user_profile,
                              resume=form.cleaned_data["resume"])
        return HttpResponse(json.dumps({"success": True}),
                            mimetype="application/json")
    return HttpResponse(json.dumps(form.errors),
                        mimetype="application/json")
