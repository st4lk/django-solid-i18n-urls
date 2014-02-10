from django.test import TestCase
from django.core.urlresolvers import clear_url_caches
try:
    from django.test.utils import TransRealMixin
except ImportError:
    class TransRealMixin(object):
        pass


class URLTestCaseBase(TransRealMixin, TestCase):

    def setUp(self):
        # Make sure the cache is empty before we are doing our tests.
        super(URLTestCaseBase, self).tearDown()
        clear_url_caches()

    def tearDown(self):
        # Make sure we will leave an empty cache for other testcases.
        clear_url_caches()
        super(URLTestCaseBase, self).tearDown()
