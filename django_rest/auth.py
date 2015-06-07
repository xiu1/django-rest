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


class HeaderAuth(BaseAuth):
    model = None
    key_model_kwarg = 'token'
    key_header_kwarg = 'x-auth-key'

    def check(self):
        header_kwarg = self.request.META.get(self.key_header_kwarg, '')
        return self.model.objects.filter(
            **{self.key_model_kwarg: header_kwarg}
        ).exists()


class UrlAuth(BaseAuth):
    model = None
    key_model_kwarg = 'api_key'
    key_url_kwarg = 'api_key'

    token_key = 'x-auth-token'

    def check(self):
        return self.model.objects.filter(
            **{self.key_model_kwarg: self.kwargs[self.key_url_kwarg]}
        ).exists()
