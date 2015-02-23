import re
from django.utils.translation import get_language
from django.core.urlresolvers import LocaleRegexURLResolver
from django.conf import settings


class SolidLocaleRegexURLResolver(LocaleRegexURLResolver):
    """
    A URL resolver that always matches the active language code as URL prefix,
    but for default language non prefix is used.

    Rather than taking a regex argument, we just override the ``regex``
    function to always return the active language-code as regex.
    """
    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        super(LocaleRegexURLResolver, self).__init__(
            None, urlconf_name, default_kwargs, app_name, namespace)

    @property
    def regex(self):
        language_code = get_language()
        if language_code not in self._regex_dict:
            if language_code != settings.LANGUAGE_CODE:
                regex = '^%s/' % language_code
            elif getattr(settings, 'SOLID_I18N_HANDLE_DEFAULT_PREFIX', False):
                regex = '(?:^%s/)?' % language_code
            else:
                regex = ''
            self._regex_dict[language_code] = re.compile(regex, re.UNICODE)
        return self._regex_dict[language_code]
