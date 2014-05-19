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
            "home": u'Здравствуйте!',
            "about": u'Информация',
        },
        "en": {
            "home": u'Hello!',
            "about": u'Information',
        }
    }

    def _base_page_check(self, response, lang_code, page_code):
        self.assertEqual(response.status_code, 200)
        content = self.PAGE_DATA[lang_code][page_code]
        self.assertTrue(content in response.content.decode('utf8'))
        self.assertEqual(response.context['LANGUAGE_CODE'], lang_code)

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
