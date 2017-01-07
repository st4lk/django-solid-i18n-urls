import sys
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
try:
    from importlib import reload  # builtin reload deprecated since version 3.4
except ImportError:
    try:
        from imp import reload
    except ImportError:
        pass
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import clear_url_caches
from django.utils import translation
try:
    from django.test.utils import TransRealMixin
except ImportError:
    class TransRealMixin(object):
        pass

from solid_i18n.urls import is_language_prefix_patterns_used


def reload_urlconf(urlconf=None, urls_attr='urlpatterns'):
    # http://codeinthehole.com/writing/how-to-reload-djangos-url-config/
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    return import_module(settings.ROOT_URLCONF)


class URLTestCaseBase(TransRealMixin, TestCase):

    def setUp(self):
        # Make sure the cache is empty before we are doing our tests.
        super(URLTestCaseBase, self).tearDown()
        clear_url_caches()
        is_language_prefix_patterns_used.cache_clear()
        reload_urlconf()

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
