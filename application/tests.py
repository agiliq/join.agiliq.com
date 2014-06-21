from django.test import TestCase
from django.core.urlresolvers import reverse
import urllib
from application.models import Application, AuthorizationCode
from user_profile.models import UserProfile
from django.contrib.auth.models import User
import urlparse
import json


class OAuthv2TestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("testuser@example.com",
                                        password="password",
                                        email="testuser@example.com")
        user_profile = UserProfile.objects.create(user=user)
        self.redirect_uri = "http://localhost:8000/oauth/callback/"
        self.application = Application.objects.create(
                                        user_profile=user_profile,
                                        client_id="TESTID",
                                        client_secret="TESTSECRET",
                                        redirect_uri=self.redirect_uri)

    def test_authorize_url_as_anonymous_user(self):
        params = {"client_id": self.application.client_id,
                  "redirect_uri": self.application.redirect_uri,
                  "response_type": "code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
               "http://testserver%s?%s" % (reverse("oauth_app_authorize"),
                                                   urllib.urlencode(params)))

    def test_authorize_url_invalid_params(self):
        params = {"client_id": self.application.client_id}
        resp = self.client.get(reverse("oauth_authorize"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "%s?%s" % ("http://testserver/",
                                    urllib.urlencode(
                                                    {"error": "invalid_client",
                                                     "error_" + \
                                     "description": "Missing Client Id"})))
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "%s?%s" % (self.redirect_uri,
                                   urllib.urlencode(
                                   {"error": "invalid_request",
                                    "error_" + \
                                   "description": "Missing Redirect URI"})))
        params.update({"client_id": self.application.client_id + "1",
                       "redirect_uri": self.application.redirect_uri})
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "%s?%s" % ("http://testserver/",
                                   urllib.urlencode(
                                   {"error": "invalid_client",
                                    "error_" + \
                                    "description": "Invalid Client Id"})))
        params.update({"client_id": self.application.client_id,
                       "redirect_uri": self.application.redirect_uri + "1"})
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "%s?%s" % (self.redirect_uri,
                                urllib.urlencode({"error": "invalid_request",
                                                     "error_" + \
                             "description": "Redirect URI does not match"})))

    def test_authorize_url_logged_in_user_confirm(self):
        self.client.login(username=self.application.user_profile.user.email,
                          password="password")
        params = {"client_id": self.application.client_id,
                  "redirect_uri": self.application.redirect_uri,
                  "response_type": "code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "http://testserver%s?%s" % (reverse(
                                                    "oauth_app_authorize"),
                                                   urllib.urlencode(params)))
        resp = self.client.post(reverse("oauth_app_authorize"),
                                {
                "authorized": "Confirm",
                "client_id": self.application.client_id,
                "redirect_uri": self.application.redirect_uri})
        self.assertEqual(resp.status_code, 302)
        query = urlparse.urlparse(resp["Location"]).query
        params = urlparse.parse_qs(query)
        self.assertTrue("code" in params)
        self.assertTrue(len(params["code"]) == 1)

    def test_authorize_url_logged_in_user_reject(self):
        self.client.login(username=self.application.user_profile.user.email,
                          password="password")
        params = {"client_id": self.application.client_id,
                  "redirect_uri": self.application.redirect_uri,
                  "response_type": "code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        resp = self.client.post(reverse("oauth_app_authorize"),
                                {
                "authorized": "Reject",
                "client_id": self.application.client_id,
                "redirect_uri": self.application.redirect_uri})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "%s?%s" % (self.application.redirect_uri,
                         urllib.urlencode(
                         {"error": "access_denied",
                         "error_description": "User " +\
                          "has rejected the authorization"})))

    def test_authorize_url_pass_state_correctly(self):
        self.client.login(username=self.application.user_profile.user.email,
                          password="password")
        params = {"client_id": self.application.client_id,
                  "redirect_uri": self.application.redirect_uri,
                  "state": "TESTSTATEVALUE",
                  "response_type": "code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_authorize"),
                                         urllib.urlencode(params)))
        resp = self.client.post(reverse("oauth_app_authorize"),
                                {
                "authorized": "Confirm",
                "client_id": self.application.client_id,
                "redirect_uri": self.application.redirect_uri,
                "state": "TESTSTATEVALUE"})
        self.assertEqual(resp.status_code, 302)
        query = urlparse.urlparse(resp["Location"]).query
        params = urlparse.parse_qs(query)
        self.assertTrue("state" in params)
        self.assertTrue(params["state"][0] == "TESTSTATEVALUE")

    def test_access_token_invalid_client_id(self):
        auth_code = AuthorizationCode.objects.create(
                       application=self.application,
                       user_profile=self.application.user_profile,
                       token="TESTTOKEN")
        params = {"client_id": self.application.client_id + "1",
                  "client_secret": self.application.client_secret,
                  "redirect_uri": self.application.redirect_uri,
                  "code": auth_code.token,
                  "grant_type": "authorization_code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_access_token"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
              resp["Location"],
              "%s?%s" % ("http://testserver/",
              urllib.urlencode(
                      {"error": "invalid_request",
                      "error_description": "Invalid Client Id"})))

    def test_access_token_invalid_client_secret(self):
        auth_code = AuthorizationCode.objects.create(
                              application=self.application,
                              user_profile=self.application.user_profile,
                              token="TESTTOKEN")
        params = {"client_id": self.application.client_id,
                  "client_secret": self.application.client_secret + "1",
                  "redirect_uri": self.application.redirect_uri,
                  "code": auth_code.token,
                  "grant_type": "authorization_code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_access_token"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
             resp["Location"],
             "%s?%s" % (self.redirect_uri,
             urllib.urlencode(
                     {"error": "invalid_request",
                     "error_description": "Invalid Client Secret"})))

    def test_access_token_invalid_redirect_uri(self):
        auth_code = AuthorizationCode.objects.create(
                              application=self.application,
                              user_profile=self.application.user_profile,
                              token="TESTTOKEN")
        params = {"client_id": self.application.client_id,
                  "client_secret": self.application.client_secret,
                  "redirect_uri": "http://example.com/",
                  "code": auth_code.token,
                  "grant_type": "authorization_code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_access_token"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
             resp["Location"],
             "%s?%s" % (self.redirect_uri,
             urllib.urlencode(
                     {"error": "invalid_request",
                     "error_description": "Redirect URI does not match"})))

    def test_access_token_invalid_code(self):
        auth_code = AuthorizationCode.objects.create(
                         application=self.application,
                         user_profile=self.application.user_profile,
                         token="TESTTOKEN")
        params = {"client_id": self.application.client_id,
                  "client_secret": self.application.client_secret,
                  "redirect_uri": self.application.redirect_uri,
                  "code": auth_code.token + "1",
                  "grant_type": "authorization_code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_access_token"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
               resp["Location"],
               "%s?%s" % (self.redirect_uri,
               urllib.urlencode(
                     {"error": "invalid_request",
                     "error_" + \
                       "description": "Invalid Authorization Code"})))

    def test_access_token_success(self):
        auth_code = AuthorizationCode.objects.create(
                            application=self.application,
                            user_profile=self.application.user_profile,
                            token="TESTTOKEN")
        params = {"client_id": self.application.client_id,
                  "client_secret": self.application.client_secret,
                  "redirect_uri": self.application.redirect_uri,
                  "code": auth_code.token,
                  "grant_type": "authorization_code"}
        resp = self.client.get("%s?%s" % (reverse("oauth_access_token"),
                                         urllib.urlencode(params)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/json")
        content = json.loads(resp.content)
        self.assertTrue(content.get("access_token") is not None)
