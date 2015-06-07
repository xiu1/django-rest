from django.conf.urls import include, url
from django.contrib import admin
from rest.views import TestRestView, TestAuthRestView

urlpatterns = [
    # Examples:
    # url(r'^$', 'rest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

    url('^rest/$', TestRestView.as_view(), name='rest'),
    url('^auth_rest/(?P<api_key>.+)/$', TestAuthRestView.as_view(), name='rest_auth'),
]
