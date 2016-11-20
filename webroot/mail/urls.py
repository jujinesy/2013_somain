#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^write/?$', 'mail.views.write', name='write'),
    url(r'^attachment/(?P<hash>[a-z0-9]+)/?$', 'mail.views.attachment', name='attachment'),
    url(r'^check/(?P<user>[a-z0-9]+)/(?P<mail>[a-z0-9]+)/?$', 'mail.views.check', name='check'),
)