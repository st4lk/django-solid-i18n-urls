# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from .base import URLTestCaseBase


class Noni18nUrlsTestCase(URLTestCaseBase):

    def test_noni18n_page(self):
        url = reverse('onelang')
        self.assertEqual(url, '/onelang/')
        response = self.client.get(url)
        self.assertContains(response, 'One language content')

    @override_settings(USE_I18N=False)
    def test_usei18n_false(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Hello!')
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'Information')
        response = self.client.get(reverse('onelang'))
        self.assertContains(response, 'One language content')
