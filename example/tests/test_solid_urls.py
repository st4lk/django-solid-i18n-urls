# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils import translation
from django.test.utils import override_settings

from .base import URLTestCaseBase


class TranslationReverseUrlTestCase(URLTestCaseBase):

    def _base_page_check(self, url_name, url_path):
        self.assertEqual(reverse(url_name), url_path)
        with translation.override('en'):
            self.assertEqual(reverse(url_name), url_path)
        with translation.override('ru'):
            self.assertEqual(reverse(url_name), '/ru' + url_path)

    # ----------- tests ----------

    def test_home_page(self):
        self._base_page_check('home', '/')

    def test_about_page(self):
        self._base_page_check('about', '/about/')

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_redirects(self):
        self._base_page_check('home', '/')

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_about_page_redirects(self):
        self._base_page_check('about', '/about/')


class TranslationAccessTestCase(URLTestCaseBase):
    PAGE_DATA = {
        "ru": {
            "home": 'Здравствуйте!',
            "about": 'Информация',
        },
        "en": {
            "home": 'Hello!',
            "about": 'Information',
        }
    }

    def _check_vary_accept_language(self, response):
        from django.conf import settings
        vary = response._headers.get('vary', ('', ''))[-1]
        if settings.SOLID_I18N_USE_REDIRECTS:
            req_path = response.request['PATH_INFO']
            if req_path.startswith('/en') or req_path.startswith('/ru'):
                self.assertFalse('Accept-Language' in vary)
            else:
                self.assertTrue('Accept-Language' in vary)
        else:
            self.assertFalse('Accept-Language' in vary)

    def _base_page_check(self, response, lang_code, page_code):
        self.assertEqual(response.status_code, 200)
        content = self.PAGE_DATA[lang_code][page_code]
        self.assertTrue(content in response.content.decode('utf8'))
        self.assertEqual(response.context['LANGUAGE_CODE'], lang_code)
        self._check_vary_accept_language(response)
        # content-language
        content_lang = response._headers.get('content-language', ('', ''))[-1]
        self.assertEqual(content_lang, lang_code)

    @property
    def en_http_headers(self):
        return dict(HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.8,ru;q=0.6')

    @property
    def ru_http_headers(self):
        return dict(HTTP_ACCEPT_LANGUAGE='ru-RU,ru;q=0.8,en;q=0.6')

    # ----------- tests ----------

    def test_home_page_en(self):
        with translation.override('en'):
            response = self.client.get(reverse('home'))
            self._base_page_check(response, "en", "home")

    def test_home_page_ru(self):
        with translation.override('ru'):
            response = self.client.get(reverse('home'))
            self._base_page_check(response, 'ru', "home")

    def test_about_page_en(self):
        with translation.override('en'):
            response = self.client.get(reverse('about'))
            self._base_page_check(response, "en", "about")

    def test_about_page_ru(self):
        with translation.override('ru'):
            response = self.client.get(reverse('about'))
            self._base_page_check(response, "ru", "about")

    def test_home_page_default_prefix_en(self):
        """
        Check, that url with explicit default language prefix is still
        accessible.
        """
        with translation.override('en'):
            response = self.client.get('/en/')
            self._base_page_check(response, "en", "home")

    def test_home_page_default_prefix_ru(self):
        """
        Check, that language is got from url prefix, even this laguage is
        not equal to client preferred langauge.
        """
        with translation.override('ru'):
            response = self.client.get('/en/')
            self._base_page_check(response, "en", "home")

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_redirects_default_lang(self):
        response = self.client.get('/', **self.en_http_headers)
        self._base_page_check(response, "en", "home")

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_redirects_non_default_lang(self):
        response = self.client.get('/', **self.ru_http_headers)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/ru/' in response['Location'])
        response = self.client.get(response['Location'], **self.ru_http_headers)
        self._base_page_check(response, 'ru', "home")

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_about_page_redirects_default_lang(self):
        response = self.client.get('/about/', **self.en_http_headers)
        self._base_page_check(response, "en", "about")

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_about_page_redirects_non_default_lang(self):
        response = self.client.get('/about/', **self.ru_http_headers)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/ru/about/' in response['Location'])
        response = self.client.get(response['Location'], **self.ru_http_headers)
        self._base_page_check(response, "ru", "about")

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_prefix_default_prefix_en(self):
        response = self.client.get('/en/', **self.en_http_headers)
        self._base_page_check(response, "en", "home")

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_prefix_default_prefix_ru(self):
        response = self.client.get('/en/', **self.ru_http_headers)
        self._base_page_check(response, "en", "home")
