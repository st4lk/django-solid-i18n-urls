import warnings
from django.conf import settings
from django.conf.urls import patterns
from django.utils import six
from .urlresolvers import SolidLocaleRegexURLResolver


def solid_i18n_patterns(prefix, *args):
    """
    Modified copy of django i18n_patterns.
    Adds the language code prefix to every *non default language* URL pattern
    within this function. This may only be used in the root URLconf,
    not in an included URLconf.
    Do not adds any language code prefix to default language URL pattern.
    Default language must be set in settings.LANGUAGE_CODE
    """
    if isinstance(prefix, six.string_types):
        warnings.warn(
            "Calling solid_i18n_patterns() with the `prefix` argument and with "
            "tuples instead of django.conf.urls.url() instances is deprecated and "
            "will no longer work in Django 2.0. Use a list of "
            "django.conf.urls.url() instances instead.",
            PendingDeprecationWarning, stacklevel=2
        )
        pattern_list = patterns(prefix, *args)
    else:
        pattern_list = [prefix] + list(args)

    if not settings.USE_I18N:
        return pattern_list
    return [SolidLocaleRegexURLResolver(pattern_list)]
