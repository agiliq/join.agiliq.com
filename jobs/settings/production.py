from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ("Shabda Raaj", "shabda@agiliq.com"),
    # ("Akshar Raaj", "akshar@agiliq.com"),
    ("Ashik S", "ashik@agiliq.com"),
)

# JOB_MANAGERS = (
#     "shabda@agiliq.com",
# )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'join_agiliq.db',        # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = get_env_variable('SECRET_KEY')
ALLOWED_HOSTS = ['join.agiliq.com', '127.0.0.1']

MEDIA_ROOT = SITE_PATH.child('media')
MEDIA_URL = "/media/"

STATIC_ROOT = SITE_PATH.child('static')
STATIC_URL = "/static/"


EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_HOST = get_env_variable('EMAIL_HOST')

# Email settings
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = "[Job]"
DEFAULT_FROM_EMAIL = "hello@agiliq.com"
