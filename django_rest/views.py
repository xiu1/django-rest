# -*- coding: utf-8 -*-

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelform_factory
from django.core import serializers
from django import http


class JsonResponse(http.HttpResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        if not isinstance(data, basestring):
            data = json.dumps(data)
        super(JsonResponse, self).__init__(content=data, **kwargs)


class RestView(View):
    model = None
    extra_get_kwarg = ['pk']
    allow_http_method = ['GET']
    auth_class = None
    response_class = None

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        # AUTH
        if self.auth_class is not None:
            auth = self.auth_class(self)
            if not auth.check():
                return http.HttpResponse(status=401)

        if self.request.method.lower() not in [m.lower() for m in self.allow_http_method]:
            return http.HttpResponseNotAllowed([m.upper() for m in self.allow_http_method])
        return super(RestView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        data = self._select()
        return JsonResponse(data)

    def post(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body)
            self._create(data)
            return http.HttpResponse(status=201)
        except:
            # TODO: not is_valid return 409
            return http.HttpResponseBadRequest()

    def put(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body)
            self._update(data)
            return JsonResponse({})
        except:
            # TODO: not is_valid return 409
            return http.HttpResponseBadRequest()

    def patch(self, *args, **kwargs):
        return self.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            self._delete()
            return JsonResponse({})
        except:
            return http.HttpResponseBadRequest()

    def get_filter(self):
        params = {}
        field_list = (self.extra_get_kwarg + self.model._meta.get_all_field_names())
        for key, values in self.request.GET.lists():
            if key.split("__")[0] not in field_list:
                continue

            if len(values) == 1:
                params[key] = values[0]
            elif len(values) > 1:
                params["{}__in".format(key)] = values
        return params

    def get_queryset(self):
        return self.model.objects.filter(**self.get_filter())

    def _select(self, **query_param):
        object_list = self.get_queryset()
        return json.dumps(list(object_list.values()), cls=DjangoJSONEncoder)
        #return serializers.serialize('json', object_list)

    def _create(self, query_param):
        form_class = modelform_factory(self.model, fields="__all__")
        form = form_class(data=query_param)
        if form.is_valid():
            return form.save()
        else:
            raise Exception("{}".form.errors)

    def _update(self, query_param):
        instance = self.get_queryset().get()
        form_class = modelform_factory(self.model, fields="__all__")
        form = form_class(data=query_param, instance=instance)
        if form.is_valid():
            return form.save()
        else:
            raise Exception("{}".form.errors)

    def _delete(self):
        if not self.get_filter():
            raise Exception('not query paramater')

        obj = self.get_queryset().get()
        obj.delete()
