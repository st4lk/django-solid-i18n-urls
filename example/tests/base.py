from django.test import TestCase
from django.core.urlresolvers import clear_url_caches


class URLTestCaseBase(TestCase):

    def setUp(self):
        # Make sure the cache is empty before we are doing our tests.
        clear_url_caches()

    def tearDown(self):
        # Make sure we will leave an empty cache for other testcases.
        clear_url_caches()
