#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', 'document.views.index', name='index'),
    url(r'^sign/(\d+)/?$', 'document.views.sign', name='sign'),
    url(r'^submit/(\d+)/?$', 'document.views.submit', name='submit'),
    url(r'^view/(\d+)/?$', 'document.views.document_view', name='view'),

    url(r'^mentoring_report/write/choose/?$', 'document.views.mentoring_report_write_choose', name='mentoring_report_write_choose'),
    url(r'^mentoring_report/write/(\d+)/?$', 'document.views.mentoring_report_write', name='mentoring_report_write'),
    url(r'^mentoring_report_list/?$', 'document.views.mentoring_report_list', name='mentoring_report_list'),
    url(r'^mentoring_report/(\d+)/?$', 'document.views.mentoring_report_view', name='mentoring_report_view'),

    url(r'^donationreceipt/write/(\d+)/?$', 'document.views.donationreceipt_write', name='donationreceipt_write'),
    url(r'^donationreceipt/(\d+)/?$', 'document.views.donationreceipt_view', name='donationreceipt_view'),
)