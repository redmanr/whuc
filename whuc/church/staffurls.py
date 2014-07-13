# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from church import views

urlpatterns = patterns('',
    url(r'^(?P<action>\w+/$)', views.staff)
)