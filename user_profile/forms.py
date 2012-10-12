from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import AuthenticationForm as AuthForm
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(max_length=50, label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, label=_("Confirm Password"),
                                widget=forms.PasswordInput)

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already " + \
                         "in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def clean(self):
        if ('password1' in self.cleaned_data and
        'password2' in self.cleaned_data):
            if (self.cleaned_data['password1'] !=
            self.cleaned_data['password2']):
                raise forms.ValidationError(_("The two password " + \
                                   "fields didn't match."))
        return self.cleaned_data


class RedirectForm(forms.Form):
    redirect_uri = forms.URLField(required=True)


class AuthenticationForm(AuthForm):
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super(AuthenticationForm, self).__init__(request, *args, **kwargs)
        self.error_messages['invalid_login'] = _("Please enter a correct email"
                                             "and password. Note that password"
                                             "is case-sensitive.")
        del self.fields["username"]

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data
