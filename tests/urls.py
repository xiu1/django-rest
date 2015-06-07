from django.conf.urls import include, url
from django.contrib import admin
from rest.views import TestRestView, TestAuthHeaderView, TestAuthUrlView

urlpatterns = [
    url('^rest/$', TestRestView.as_view(), name='rest'),
    url('^auth_header_rest/$', TestAuthHeaderView.as_view(), name='rest_auth_header'),
    url('^auth_url_rest/(?P<api_key>.+)/$', TestAuthUrlView.as_view(), name='rest_auth_url'),
]
