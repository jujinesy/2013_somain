#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # member/profile/ 관련 url
    url(r'^profile/$', 'member.views.profile', name='profile'),
    url(r'^profile/(\d+)/$', 'member.views.profile', name='profile'),
    url(r'^profile/add_award/$', 'member.views.add_award', name='add_award'),
    url(r'^profile/delete_award/(\d+)/$', 'member.views.delete_award', name='delete_award'),
    url(r'^profile/delete_career/(\d+)/$', 'member.views.delete_career', name='delete_career'),
    url(r'^profile/add_career/$', 'member.views.add_career', name='add_career'),
)