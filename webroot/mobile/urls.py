#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'mobile.api.login', name='login'),
    url(r'^document/$', 'mobile.api.document', name='document'),
    url(r'^document_list/$', 'mobile.api.document_list', name='document_list'),
    url(r'^notice_list/$', 'mobile.api.notice_list', name='notice_list'),
    url(r'^sign/$', 'mobile.api.sign', name='sign'),

    url(r'^reg_android/$', 'mobile.api.registration_android', name='reg_android'),
    url(r'^send_gcm/$', 'mobile.api.send_gcm', name='send_gcm'),
)