#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^search$', 'korzip.views.search', name='search'),    
    url(r'^test$', 'korzip.views.test', name='test'),    
)