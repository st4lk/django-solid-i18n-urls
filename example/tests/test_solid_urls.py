# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils import translation

from base import URLTestCaseBase


class TranslationReverseUrlTestCase(URLTestCaseBase):

    def test_home_page(self):
        self.assertEqual(reverse('home'), '/')
        with translation.override('en'):
            self.assertEqual(reverse('home'), '/')
        with translation.override('ru'):
            self.assertEqual(reverse('home'), '/ru/')

    def test_about_page(self):
        self.assertEqual(reverse('about'), '/about/')
        with translation.override('en'):
            self.assertEqual(reverse('about'), '/about/')
        with translation.override('ru'):
            self.assertEqual(reverse('about'), '/ru/about/')


class TranslationAccessTestCase(URLTestCaseBase):

    def test_home_page(self):
        with translation.override('en'):
            response = self.client.get(reverse('home'))
            self.assertContains(response, 'Hello!')
            self.assertEqual(response.context['LANGUAGE_CODE'], 'en')
        with translation.override('ru'):
            response = self.client.get(reverse('home'))
            self.assertTrue(response.status_code, 200)
            self.assertTrue(u'Здравствуйте!', response.content.decode('utf8'))
            self.assertEqual(response.context['LANGUAGE_CODE'], 'ru')

    def test_about_page(self):
        with translation.override('en'):
            response = self.client.get(reverse('about'))
            self.assertContains(response, 'Information')
            self.assertEqual(response.context['LANGUAGE_CODE'], 'en')
        with translation.override('ru'):
            response = self.client.get(reverse('about'))
            self.assertTrue(response.status_code, 200)
            self.assertTrue(u'Информация', response.content.decode('utf8'))
            self.assertEqual(response.context['LANGUAGE_CODE'], 'ru')
