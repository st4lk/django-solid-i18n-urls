from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.urlresolvers import get_resolver
from django.http import HttpResponseRedirect
from django.utils.cache import cc_delim_re
from django.utils import translation as trans
from django.middleware.locale import LocaleMiddleware
from django.utils.datastructures import SortedDict
from .urlresolvers import SolidLocaleRegexURLResolver


django_root_version = DJANGO_VERSION[0]*10 + DJANGO_VERSION[1]


def unpatch_vary_headers(response, removeheaders):
    """
    Removes specified entries from the "Vary" header in the given
    HttpResponse object. Other existing headers in "Vary" aren't removed.
    """
    # Note that we need to keep the original order intact, because cache
    # implementations may rely on the order of the Vary contents in, say,
    # computing an MD5 hash.
    if response.has_header('Vary'):
        vary_headers = cc_delim_re.split(response['Vary'])
    else:
        vary_headers = []
    removeheaders_lower = [h.lower() for h in removeheaders]
    updated_headers = [header for header in vary_headers
                       if header.lower() not in removeheaders_lower]
    response['Vary'] = ', '.join(updated_headers)


class SolidLocaleMiddleware(LocaleMiddleware):
    """
    Request without language prefix will use default language.
    Or, if settings.SOLID_I18N_USE_REDIRECTS is True, try to discover language.
    If language is not equal to default language, redirect to discovered
    language.

    If request contains language prefix, this language will be used immediately.
    In that case settings.SOLID_I18N_USE_REDIRECTS doesn't make sense.

    Default language is set in settings.LANGUAGE_CODE.
    """

    def __init__(self):
        self._supported_languages = SortedDict(settings.LANGUAGES)
        self._is_language_prefix_patterns_used = False
        for url_pattern in get_resolver(None).url_patterns:
            if isinstance(url_pattern, SolidLocaleRegexURLResolver):
                self._is_language_prefix_patterns_used = True
                break

    @property
    def use_redirects(self):
        return getattr(settings, 'SOLID_I18N_USE_REDIRECTS', False)

    @property
    def default_lang(self):
        return settings.LANGUAGE_CODE

    def process_request(self, request):
        check_path = self.is_language_prefix_patterns_used()
        if check_path and not self.use_redirects:
            language = trans.get_language_from_path(request.path_info)
            language = language or self.default_lang
        else:
            language = trans.get_language_from_request(request, check_path)
        trans.activate(language)
        request.LANGUAGE_CODE = trans.get_language()

    def process_response(self, request, response):
        language = trans.get_language()
        if self.use_redirects:
            rr_response = super(SolidLocaleMiddleware, self).\
                process_response(request, response)
            if rr_response:
                if not isinstance(rr_response, HttpResponseRedirect):
                    if django_root_version < 16 and language != self.default_lang:
                        unpatch_vary_headers(rr_response, ("Accept-Language", ))
                    return rr_response
                elif language != self.default_lang:
                    return rr_response
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response

    def is_language_prefix_patterns_used(self):
        """
        Returns `True` if the `SolidLocaleRegexURLResolver` is used
        at root level of the urlpatterns, else it returns `False`.
        """
        return self._is_language_prefix_patterns_used
