"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import urlparse
import StringIO

from django.test import TestCase, client
from django.conf import settings
from django.contrib.auth.models import User
from application.models import Application
from application.models import  AccessToken
from user_profile.models import UserProfile


class APIViewsTestCase(TestCase):
    """
    Test cases for 'api.views'
    """
    def setUp(self):
        """
        initializes required variables to perform tests.
        """
        user = User.objects.create_user("testuser@example.com",
                                        password="password",
                                        email="testuser@example.com")
        user_profile = UserProfile.objects.create(user=user)
        self.redirect_uri = "http://localhost:8000/oauth/callback/"
        self.application = Application.objects.create(
                                user_profile=user_profile,
                                client_id="TESTID",
                                client_secret="TESTSECRET",
                                redirect_uri=self.redirect_uri
                            )
        self.access_token = AccessToken.objects.create(
                                user_profile=user_profile,
                                application=self.application,
                                token="abcd"
                            )
        f = StringIO.StringIO("Contains Dummy Text")
        f.name = "resume.pdf"
        self.data = {'first_name': 'FirstName',
                    'last_name': 'LastName',
                    'projects_url': 'http://www.example.com/name/projects/',
                    'code_url': 'http://www.example.com/name/projects/1/code/',
                    'resume': f,
                }

    def test_resume_upload(self):
        """
        ``test_resume_upload`` will make a multipart post request. If this
        test Fails it raises an ``AssertionError``
        """
        settings.JOB_MANAGERS = []
        resp = self.client.post(
                '/api/resume/upload/?access_token=%s' % \
                    self.access_token.token,
                self.data
                )
        self.assertEqual(resp.status_code, 200)
        resp_content = json.loads(resp.content)['success']
        self.assertEqual(resp_content, True)

    def test_resume_upload_missing_access_token(self):
        """
        ``test_resume_upload_missing_access_token`` will send the data missing
        access token. It raises ``AssertionError``s if this fails.
        """
        resp = self.client.post('/api/resume/upload/', self.data)
        self.assertEqual(resp.status_code, 302)
        parsed_url = urlparse.urlparse(resp['Location'])
        resp_dict = urlparse.parse_qs(parsed_url.query)
        self.assertEqual(resp_dict['error_description'], \
                                    ["Missing Access Token"])
        self.assertEqual(resp_dict['error'], ["invalid_request"])

    def test_resume_upload_invalid_access_token(self):
        """
        ``test_resume_upload_invalid_access_token`` will send an invalid access
        token to the system.
        """
        resp = self.client.post('/api/resume/upload/?access_token=1234',\
                self.data)
        self.assertEqual(resp.status_code, 302)

    def test_resume_upload_no_resume(self):
        """
        ``test_resume_upload_no_resume`` will test for the ``resume`` in data.
        """
        temp_data = self.data.copy()
        del temp_data['resume']
        resp = self.client.post('/api/resume/upload/?access_token=%s' % \
                self.access_token.token, temp_data)
        resp_content = json.loads(resp.content)['resume']
        self.assertEqual(resp_content, ["This field is required."])

    def test_resume_upload_invalid_projects_url(self):
        """
        ``test_resume_upload_invalid_projects_url`` will check for valid
        projects url.
        """
        temp_data = self.data.copy()
        temp_data['projects_url'] = 'abcdefg'
        resp = self.client.post('/api/resume/upload/?access_token=%s' % \
                self.access_token.token, temp_data)
        resp_content = json.loads(resp.content)['projects_url']
        self.assertEqual(resp_content, ["Enter a valid URL."])

    def test_resume_upload_invalid_code_url(self):
        """
        ``test_resume_upload_invalid_code_url`` will check for valid code url.
        """
        temp_data = self.data.copy()
        temp_data['code_url'] = 'abcdefg'
        resp = self.client.post('/api/resume/upload/?access_token=%s' % \
                self.access_token.token, temp_data)

        resp_content = json.loads(resp.content)['code_url']
        self.assertEqual(resp_content, ["Enter a valid URL."])
