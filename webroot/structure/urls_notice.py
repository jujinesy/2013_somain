#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', 'structure.views_notice.list', name='list'),
    url(r'^(\d+)/$', 'structure.views_notice.detail', name='detail'),
    url(r'^add/$', 'structure.views_notice.add_notice', name='add'),
)