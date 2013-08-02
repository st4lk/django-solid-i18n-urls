from django.conf import settings
from django.core.urlresolvers import get_resolver
from django.utils.cache import patch_vary_headers
from django.utils import translation
from urlresolvers import SolidLocaleRegexURLResolver


class SolidLocaleMiddleware(object):
    """
    This is a modified copy of django LocaleMiddleware.
    It doesn't use redirects at all.
    Requests without language prefix treated as request with default language.
    Default language is set in settings.LANGUAGE_CODE.
    Request with non default language prefix treated similiar to
    LocaleMiddleware.
    """

    def process_request(self, request):
        if self.is_language_prefix_patterns_used():
            language = translation.get_language_from_path(request.path_info)
            language = language or settings.LANGUAGE_CODE
        else:
            language = translation.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        translation.deactivate()

        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response

    def is_language_prefix_patterns_used(self):
        """
        Returns `True` if the `SolidLocaleRegexURLResolver` is used
        at root level of the urlpatterns, else it returns `False`.
        """
        for url_pattern in get_resolver(None).url_patterns:
            if isinstance(url_pattern, SolidLocaleRegexURLResolver):
                return True
        return False
