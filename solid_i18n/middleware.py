from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.urlresolvers import get_resolver
from django.http import HttpResponseRedirect
from django.utils.cache import patch_vary_headers
from django.utils import translation as trans
from django.middleware.locale import LocaleMiddleware
from django.utils.datastructures import SortedDict
from django.utils import translation
from .urlresolvers import SolidLocaleRegexURLResolver


django_root_version = DJANGO_VERSION[0]*10 + DJANGO_VERSION[1]


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
        kwargs = {}
        if self.use_redirects:
            rr_response = super(SolidLocaleMiddleware, self).\
                process_response(request, response)
            if rr_response and not(
                    isinstance(rr_response, HttpResponseRedirect)
                    and language == self.default_lang):
                return rr_response

        if django_root_version >= 16:
            kwargs["supported"] = self._supported_languages
        language_from_path = translation.get_language_from_path(
            request.path_info, **kwargs)
        if not (self.is_language_prefix_patterns_used()
                and language_from_path):
            patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response

    def is_language_prefix_patterns_used(self):
        """
        Returns `True` if the `SolidLocaleRegexURLResolver` is used
        at root level of the urlpatterns, else it returns `False`.
        """
        return self._is_language_prefix_patterns_used
