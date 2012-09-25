from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(max_length=50, label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, label=_("Confirm Password"),
                                widget=forms.PasswordInput)

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class RedirectForm(forms.Form):
    redirect_uri = forms.URLField(required=True)
