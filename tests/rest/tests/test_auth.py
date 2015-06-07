# -*- coding: utf-8 -*-

import json
import uuid
from django.test import TestCase
from django.core.urlresolvers import reverse

from rest.models import RestModel, AuthModel


class HeaderAuthTest(TestCase):
    def setUp(self):
        self.api_key = "{}".format(uuid.uuid4()).replace('-', '')
        AuthModel.objects.create(api_key=self.api_key)

    def test_get_reject(self):
        api_key = "{}".format(uuid.uuid4()).replace('-', '')
        res = self.client.get(reverse('rest_auth_header'), **{'x-auth-key': api_key})
        self.assertNotEqual(res.status_code, 200)

    def test_get_accept(self):
        RestModel.objects.create(name="test", number=10)
        res = self.client.get(reverse('rest_auth_header'), **{'x-auth-key': self.api_key})
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(RestModel.objects.all(), ['<RestModel: test>'])


class UrlAuthTest(TestCase):
    def setUp(self):
        self.api_key = "{}".format(uuid.uuid4()).replace('-', '')
        AuthModel.objects.create(api_key=self.api_key)

    def test_get_reject(self):
        api_key = "{}".format(uuid.uuid4()).replace('-', '')
        res = self.client.get(reverse('rest_auth_url', kwargs={'api_key': api_key}))
        self.assertNotEqual(res.status_code, 200)

    def test_get_accept(self):
        RestModel.objects.create(name="test", number=10)
        res = self.client.get(reverse('rest_auth_url', kwargs={'api_key': self.api_key}))
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(RestModel.objects.all(), ['<RestModel: test>'])
