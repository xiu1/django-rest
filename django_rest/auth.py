# -*- coding: utf-8 -*-


class BaseAuth(object):
    def __init__(self, klass):
        self.kwargs = klass.kwargs
        self.request = klass.request
        self.klass = klass

    # It must override
    # return True: Accept, False: Reject
    def check(self):
        return False


class ApiKeyAuth(BaseAuth):
    model = None
    key_model_kwarg = 'api_key'
    key_url_kwarg = 'api_key'

    def check(self):
        return self.model.objects.filter(
            **{self.key_model_kwarg: self.kwargs[self.key_url_kwarg]}
        ).exists()
