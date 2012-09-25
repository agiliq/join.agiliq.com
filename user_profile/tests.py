from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from registration.models import RegistrationProfile
from application.models import Application

class UserProfileTestCase(TestCase):
    def test_signup(self):
        resp = self.client.post(reverse("registration_register"),
                                {"email": "testuser@example.com",
                                 "password1": "password",
                                 "password2": "password"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "http://testserver%s" % reverse("registration_complete"))
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.username, "testuser@example.com")
        self.assertEqual(user.email, "testuser@example.com")
        user_profile = UserProfile.objects.get()
        self.assertEqual(user_profile.user, user)

    def test_activate_account(self):
        resp = self.client.post(reverse("registration_register"),
                                {"email": "testuser@example.com",
                                 "password1": "password",
                                 "password2": "password"})
        user = User.objects.get()
        self.assertEqual(user.is_active, False)
        self.assertEqual(Application.objects.count(), 0)
        rp = RegistrationProfile.objects.get()
        resp = self.client.get(reverse("registration_activate",
                                       kwargs={"activation_key": rp.activation_key}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"],
                         "http://testserver%s" % reverse("registration_activation_complete"))
        user = User.objects.get()
        self.assertEqual(user.is_active, True)
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.get()
        self.assertEqual(application.user_profile, user.get_profile())

    def test_login(self):
        resp = self.client.post(reverse("registration_register"),
                                {"email": "testuser@example.com",
                                 "password1": "password",
                                 "password2": "password"})
        user = User.objects.get()
        user.is_active = True
        user.save()
        resp = self.client.post(reverse("auth_login"),
                                {"username": "testuser@example.com",
                                 "password": "password"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], 
                         "http://testserver%s" % reverse("user_profile_home"))
