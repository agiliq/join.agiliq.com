from django import forms

class OAuthApplicationAuthorizationForm(forms.Form):
    client_id = forms.CharField(max_length=50, widget=forms.HiddenInput())
    redirect_uri = forms.URLField(widget=forms.HiddenInput())
    state = forms.CharField(max_length=100, widget=forms.HiddenInput(), required=False)
