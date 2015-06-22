from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from myxpense.api import *
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(ExpenseResource())
v1_api.register(ExpenseBookResource())
v1_api.register(PersonResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', 'myxpense.views.index', name='index'),
    url(r'^login', 'myxpense.views.login', name='login'),
    url(r'^logout', 'myxpense.views.logout', name='logout'),
    url(r'^signup', 'myxpense.views.signup', name='signup'),
    url(r'^app', 'myxpense.views.app', name='app'),
)
