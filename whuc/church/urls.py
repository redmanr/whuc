# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from church import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^(?P<action>\w+/$)', views.action)
)