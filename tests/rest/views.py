# -*- coding: utf-8 -*-

from django_rest.views import RestView
from django_rest.auth import HeaderAuth, UrlAuth
from rest.models import RestModel, AuthModel


class TestRestView(RestView):
    model = RestModel
    allow_http_method = ['GET', 'POST', 'PUT', 'DELETE']


class TestHeaderAuth(HeaderAuth):
    model = AuthModel
    key_model_kwarg = 'api_key'


class TestAuthHeaderView(RestView):
    model = RestModel
    auth_class = TestHeaderAuth


class TestUrlAuth(UrlAuth):
    model = AuthModel


class TestAuthUrlView(RestView):
    model = RestModel
    auth_class = TestUrlAuth
