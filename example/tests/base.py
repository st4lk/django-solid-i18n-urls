from django.test import TestCase
from django.core.urlresolvers import clear_url_caches
from django.utils import translation
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
        # Not sure why exactly, but TransRealMixin was removied in django 1.7
        # look https://github.com/django/django/commit/b87bc461c89f2006f0b27c7240fb488fac32bed1
        # Without it, tests will fail with django 1.7, because language
        # will be kept in _active.value between tests.
        # have to delete _active.value explicitly by calling deactivate
        # TODO: investigate this problem more deeply
        translation.deactivate()
        super(URLTestCaseBase, self).tearDown()
