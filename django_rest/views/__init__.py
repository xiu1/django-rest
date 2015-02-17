import json

from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.forms.models import modelform_factory
from django.core import serializers

from django.http import HttpResponse, HttpResponseBadRequest
"""
try:
    from django.http import JsonResponse
except ImportError:
    pass
    # TODO: django 1.8-
"""

class JsonResponse(HttpResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        if not isinstance(data, basestring):
            data = json.dumps(data)
        super(JsonResponse, self).__init__(content=data, **kwargs)


class RestView(View):
    model = None
    queryset = None
    pk_url_kwarg = 'pk'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        # TODO: API auth
        return super(RestView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        data = self.__select()
        return JsonResponse(data)

    def post(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body)
            self.__create(data)
            return HttpResponse(status=201)
        except Exception as e:
            print(e)
        return HttpResponseBadRequest()

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body)
        self.__update(data)
        return JsonResponse({})

    def patch(self, *args, **kargs):
        return self.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.__delete()
        return JsonResponse({})

    def get_filter(self):
        params = {}
        field_list = ([self.pk_url_kwarg, self.slug_url_kwarg]
                      + self.model._meta.get_all_field_names())
        for key, values in self.request.GET.lists():
            # key check 
            if key.split("__")[0] not in field_list:
                continue

            if len(values) == 1:
                params[key] = values[0]
            elif len(values) > 1:
                params["{}__in".format(key)] = values
        return params

    def get_queryset(self):
        return self.model.objects.filter(**self.get_filter())

    def __select(self, **query_param):
        object_list = self.get_queryset()
        return serializers.serialize('json', object_list)

    def __create(self, query_param):
        form_class = modelform_factory(self.model, fields="__all__")
        form = form_class(data=query_param)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            raise Exception("error")
            # TODO: error response
        return form


    def __update(self, query_param):
        try:
            instance = self.get_queryset().get()
            form_class = modelform_factory(self.model, fields="__all__")
            form = form_class(data=query_param, instance=instance)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        except Exception as e:
            print(e)
            pass
        return

    def __delete(self):
        try:
            obj = self.get_queryset().get()
            obj.delete()
        except Exception as e:
            print(e)
            pass
            # faile
        return
