from .settings import *
from django import VERSION

if VERSION < (1, 8):
    INSTALLED_APPS += (
        'django_nose',
    )

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'TEST_CHARSET': 'utf8',
    }}
