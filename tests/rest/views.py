# -*- coding: utf-8 -*-

from django_rest.views import RestView
from django_rest.auth import ApiKeyAuth
from rest.models import RestModel, AuthModel


class TestRestView(RestView):
    model = RestModel
    allow_http_method = ['GET', 'POST', 'PUT', 'DELETE']


class TestApiKeyAuth(ApiKeyAuth):
    model = AuthModel


class TestAuthRestView(RestView):
    model = RestModel
    auth_class = TestApiKeyAuth
