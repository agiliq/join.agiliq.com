from django import forms

class ResumeUploadForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    resume = forms.FileField()
