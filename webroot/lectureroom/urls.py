#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'lectureroom.views.main', name='main'),
    url(r'^my/?$', 'lectureroom.views.mylist', name='mylist'),
    url(r'^list/?$', 'lectureroom.views.list', name=''),
    url(r'^new/?$', 'lectureroom.views.new', name='new'),
    url(r'^new/check/?$', 'lectureroom.views.check', name='check'),
    url(r'^new/recent/?$', 'lectureroom.views.recent', name='recent'),
    url(r'^delete/?$', 'lectureroom.views.delete', name='delete'),
    url(r'^view/(\d+)/?$', 'lectureroom.views.view', name='view'),
)