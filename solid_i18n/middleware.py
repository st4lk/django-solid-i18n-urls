from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.urlresolvers import get_resolver, is_valid_path
from django.http import HttpResponseRedirect
from django.utils.cache import patch_vary_headers
from django.utils import translation as trans
from django.middleware.locale import LocaleMiddleware
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
    response_redirect_class = HttpResponseRedirect

    def __init__(self):
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
        language = translation.get_language()
        if self.use_redirects:
            language_from_path = translation.get_language_from_path(
                request.path_info)
            if (response.status_code == 404 and not language_from_path
                    and self.is_language_prefix_patterns_used()
                    and language != self.default_lang):
                urlconf = getattr(request, 'urlconf', None)
                language_path = '/%s%s' % (language, request.path_info)
                path_valid = is_valid_path(language_path, urlconf)
                if (not path_valid and settings.APPEND_SLASH
                        and not language_path.endswith('/')):
                    path_valid = is_valid_path("%s/" % language_path, urlconf)

                if path_valid:
                    if django_root_version >= 17:
                        scheme = request.scheme
                    else:
                        scheme = 'https' if request.is_secure() else 'http'
                    language_url = "%s://%s/%s%s" % (
                        scheme, request.get_host(), language,
                        request.get_full_path())
                    return self.response_redirect_class(language_url)

            if not (self.is_language_prefix_patterns_used()
                    and language_from_path):
                patch_vary_headers(response, ('Accept-Language',))
            if django_root_version < 16:
                translation.deactivate()
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response

    def is_language_prefix_patterns_used(self):
        """
        Returns `True` if the `SolidLocaleRegexURLResolver` is used
        at root level of the urlpatterns, else it returns `False`.
        """
        return self._is_language_prefix_patterns_used
