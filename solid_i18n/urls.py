from django.conf import settings
from django.conf.urls import patterns
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
    pattern_list = patterns(prefix, *args)
    if not settings.USE_I18N:
        return pattern_list
    return [SolidLocaleRegexURLResolver(pattern_list)]
