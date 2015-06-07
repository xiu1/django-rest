# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class RestModel(models.Model):
    name = models.CharField(max_length=32)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AuthModel(models.Model):
    api_key = models.TextField()

    def __str__(self):
        return self.name
