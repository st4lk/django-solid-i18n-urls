import re

from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.urlresolvers import (is_valid_path, get_resolver,
    get_script_prefix)
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.utils.cache import patch_vary_headers
from django.utils import translation as trans
from django.utils.translation.trans_real import language_code_prefix_re
from django.middleware.locale import LocaleMiddleware
from django.utils.functional import cached_property

from .urlresolvers import SolidLocaleRegexURLResolver
from .memory import set_language_from_path
from .contrib import get_full_path

strict_language_code_prefix_re = re.compile(
    r'^/({0})(/|$)'.format(
        '|'.join(
            map(
                re.escape,
                dict(settings.LANGUAGES).keys()
            )
        )
    ),
    flags=re.IGNORECASE
)

def get_language_from_path(path):
    """
    django.utils.translation wrapper does't allow/pass strict argument
    """
    if settings.USE_I18N:
        strict = getattr(settings, 'SOLID_I18N_PREFIX_STRICT', False)
        if strict and not strict_language_code_prefix_re.match(path):
            return None
        # strict below could possibly be removed since the above is in place
        return trans.trans_real.get_language_from_path(path, strict=strict)


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
    response_default_language_redirect_class = HttpResponsePermanentRedirect

    @property
    def use_redirects(self):
        return getattr(settings, 'SOLID_I18N_USE_REDIRECTS', False)

    @property
    def default_lang(self):
        return settings.LANGUAGE_CODE

    def process_request(self, request):
        check_path = self.is_language_prefix_patterns_used
        language_path = get_language_from_path(request.path_info)
        if check_path and not self.use_redirects:
            language = language_path or self.default_lang
        else:
            language = trans.get_language_from_request(request, check_path)
        set_language_from_path(language_path)
        trans.activate(language)
        request.LANGUAGE_CODE = trans.get_language()

    def process_response(self, request, response):
        language = trans.get_language()
        language_from_path = get_language_from_path(request.path_info)
        if (getattr(settings, 'SOLID_I18N_DEFAULT_PREFIX_REDIRECT', False)
                and language_from_path == self.default_lang
                and self.is_language_prefix_patterns_used):
            redirect = self.perform_redirect(request, '', is_permanent=True)
            if redirect:
                return redirect
        elif self.use_redirects:
            if (response.status_code == 404 and not language_from_path
                    and self.is_language_prefix_patterns_used
                    and language != self.default_lang):
                redirect = self.perform_redirect(request, language)
                if redirect:
                    return redirect
            if not (self.is_language_prefix_patterns_used
                    and language_from_path):
                patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response

    def remove_lang_from_path(self, path):
        no_lang_tag_path = path
        regex_match = language_code_prefix_re.match(path)
        if regex_match:
            lang_code = regex_match.group(1)
            no_lang_tag_path = path[1 + len(lang_code):]
            if not no_lang_tag_path.startswith('/'):
                no_lang_tag_path = '/' + no_lang_tag_path
        return no_lang_tag_path

    def perform_redirect(self, request, language, is_permanent=False):
        # language can be empty string (in case of default language)
        path_info = request.path_info
        if not language:
            path_info = self.remove_lang_from_path(path_info)
        urlconf = getattr(request, 'urlconf', None)
        language_path = '%s%s' % (language, path_info)
        if not language_path.startswith('/'):
            language_path = '/' + language_path
        path_valid = is_valid_path(language_path, urlconf)
        path_needs_slash = (
            not path_valid and (
                settings.APPEND_SLASH and not language_path.endswith('/')
                and is_valid_path('%s/' % language_path, urlconf)
            )
        )

        if path_valid or path_needs_slash:
            script_prefix = get_script_prefix()
            if DJANGO_VERSION < (1, 9):
                full_path = get_full_path(request, force_append_slash=path_needs_slash)
            else:
                full_path = request.get_full_path(force_append_slash=path_needs_slash)
            if not language:
                full_path = self.remove_lang_from_path(full_path)
            language_url = full_path.replace(
                script_prefix,
                '%s%s/' % (script_prefix, language) if language else script_prefix,
                1
            )

            # return a 301 permanent redirect if on default language
            if (is_permanent):
                return self.response_default_language_redirect_class(language_url)
            else:
                return self.response_redirect_class(language_url)

    @cached_property
    def is_language_prefix_patterns_used(self):
        """
        Returns `True` if the `SolidLocaleRegexURLResolver` is used
        at root level of the urlpatterns, else it returns `False`.
        """
        for url_pattern in get_resolver(None).url_patterns:
            if isinstance(url_pattern, SolidLocaleRegexURLResolver):
                return True
        return False
