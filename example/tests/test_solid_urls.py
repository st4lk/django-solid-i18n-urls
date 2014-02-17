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

    def _base_check_home_en(self, response):
        self.assertContains(response, 'Hello!')
        self.assertEqual(response.context['LANGUAGE_CODE'], 'en')

    def _base_check_home_ru(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Здравствуйте!' in response.content.decode('utf8'))
        self.assertEqual(response.context['LANGUAGE_CODE'], 'ru')

    def _base_check_about_en(self, response):
        self.assertContains(response, 'Information')
        self.assertEqual(response.context['LANGUAGE_CODE'], 'en')

    def _base_check_about_ru(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Информация' in response.content.decode('utf8'))
        self.assertEqual(response.context['LANGUAGE_CODE'], 'ru')

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
            self._base_check_home_en(response)

    def test_home_page_ru(self):
        with translation.override('ru'):
            response = self.client.get(reverse('home'))
            self._base_check_home_ru(response)

    def test_about_page_en(self):
        with translation.override('en'):
            response = self.client.get(reverse('about'))
            self._base_check_about_en(response)

    def test_about_page_ru(self):
        with translation.override('ru'):
            response = self.client.get(reverse('about'))
            self._base_check_about_ru(response)

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_redirects_default_lang(self):
        response = self.client.get('/', **self.en_http_headers)
        self._base_check_home_en(response)

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_home_page_redirects_non_default_lang(self):
        response = self.client.get('/', **self.ru_http_headers)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/ru/' in response['Location'])
        response = self.client.get(response['Location'], **self.ru_http_headers)
        self._base_check_home_ru(response)

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_about_page_redirects_default_lang(self):
        response = self.client.get('/about/', **self.en_http_headers)
        self._base_check_about_en(response)

    @override_settings(SOLID_I18N_USE_REDIRECTS=True)
    def test_about_page_redirects_non_default_lang(self):
        response = self.client.get('/about/', **self.ru_http_headers)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/ru/about/' in response['Location'])
        response = self.client.get(response['Location'], **self.ru_http_headers)
        self._base_check_about_ru(response)
