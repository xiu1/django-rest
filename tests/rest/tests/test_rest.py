# -*- coding: utf-8 -*-

import json
import uuid
from django.test import TestCase
from django.core.urlresolvers import reverse

from rest.models import RestModel


class RestSuccessTest(TestCase):
    def test_select(self):
        res = self.client.get(reverse('rest'))
        body = json.loads(res.content)
        self.assertEqual(body, [])

        RestModel.objects.create(name="test", number=1)
        res = self.client.get(reverse('rest'))
        body = json.loads(res.content)
        self.assertEqual(len(body), RestModel.objects.all().count())
        self.assertEqual(body[0]['name'], "test")
        self.assertEqual(body[0]['number'], 1)

    def test_create(self):
        data = json.dumps({
            'name': 'post_data',
            'number': 123
        })
        res = self.client.post(reverse('rest'), content_type='application/json', data=data)
        self.assertEqual(res.status_code, 201)
        self.assertQuerysetEqual(RestModel.objects.all(), ['<RestModel: post_data>'])

        res = self.client.get(reverse('rest'), data={'name': 'post_data'})
        body = json.loads(res.content)
        self.assertEqual(len(body), RestModel.objects.all().count())
        self.assertEqual(len(body), RestModel.objects.all().count())
        self.assertEqual(body[0]['name'], "post_data")
        self.assertEqual(body[0]['number'], 123)

    def test_update(self):
        instance = RestModel.objects.create(name="test_update", number=123)
        data = json.dumps({
            'name': 'test_update2',
            'number': 456
        })
        res = self.client.put(
            "{}?id={}".format(reverse('rest'), instance.id),
            content_type='application/json', data=data
        )
        self.assertEqual(res.status_code, 201)
        self.assertQuerysetEqual(
            RestModel.objects.filter(id=instance.id),
            ['<RestModel: test_update2>']
        )

    def test_delete(self):
        instance = RestModel.objects.create(name="test_delete", number=123)
        res = self.client.delete(
            "{}?id={}".format(reverse('rest'), instance.id),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 204)
        self.assertQuerysetEqual(RestModel.objects.all(), [])


class RestFailTest(TestCase):
    def test_create(self):
        data = json.dumps({
            'name': 'post_data',
        })
        res = self.client.post(reverse('rest'), content_type='application/json', data=data)
        self.assertEqual(res.status_code, 400)
        self.assertQuerysetEqual(RestModel.objects.all(), [])

    def test_update(self):
        instance = RestModel.objects.create(name="test_update", number=123)
        data = json.dumps({
            'name': 'test_update2',
        })
        res = self.client.put(
            "{}?id={}".format(reverse('rest'), instance.id),
            content_type='application/json', data=data
        )
        self.assertEqual(res.status_code, 400)
        self.assertQuerysetEqual(
            RestModel.objects.filter(id=instance.id),
            ['<RestModel: test_update>']
        )

    def test_delete(self):
        RestModel.objects.create(name="test_delete", number=123)
        res = self.client.delete(reverse('rest'))
        self.assertNotEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            RestModel.objects.all(), ['<RestModel: test_delete>']
        )
