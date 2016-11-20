#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', 'manager.views.index', name='index'),
    url(r'^login/?$', auth_views.login, 
        {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/?$', auth_views.logout,
        {'template_name': 'registration/logout.html'}, name='logout'),

    # User list
    url(r'^userlist/?$', 'manager.views.userlist', name='userlist'),
    url(r'^modify_userlist/?$', 'manager.views.modify_userlist', name='modify_userlist'),

    url(r'^user_profile/(\d+)/?$', 'manager.views.user_profile', name='user_profile'),
    url(r'^convert/?$', 'manager.views.convert', name='convert'),

    # Mail
    url(r'^mail/staff/?$', 'manager.views.mail_staff', name='mail_staff'),
    url(r'^mail/staff/edit/?$', 'manager.views.edit_mail_staff', name='edit_mail_staff'),
    url(r'^mail/check/?$', 'manager.views.mail_check', name='mail_check'),

    # Document

    # Document-index
    url(r'^document/?$', 'manager.views_document.index', name='document_index'),
    url(r'^document/mentoringreport/?$', 'manager.views_document.mentoringreport', name='document_mentoringreport'),
    url(r'^document/mentoringreport/excel/?$', 'manager.views.convert_mentoringreport', name='convert_mentoringreport'),

    # Document - DonationReceipt
    #url(r'^document/donationreceipt/?$', 'manager.views_document.donationreceipt', name='document_donationreceipt'),
    url(r'^document/donationreceipt/create/?$', 'manager.views_document_donationreceipt.create_donationreceipt', name='document_donationreceipt_create'),
    url(r'^document/donationreceipt/report/?$', 'manager.views_document_donationreceipt.donationreceipt_report', name='document_donationreceipt_report'),

    # Notice
    url(r'^notice/$', 'manager.views_notice.list', name='notice'),
    url(r'^notice/(\d+)/$', 'manager.views_notice.detail', name='notice_detail'),
    url(r'^notice/add/$', 'manager.views_notice.add_notice', name='notice_add'),
    url(r'^notice/edit/(\d+)/$', 'manager.views_notice.edit_notice', name='notice_edit'),
    url(r'^notice/category/$', 'manager.views_notice.category_list', name='notice_category'),
    url(r'^notice/category/(\d+)/$', 'manager.views_notice.category_detail', name='notice_category_detail'),
    url(r'^notice/category/edit/(\d+)/$', 'manager.views_notice.edit_category', name='notice_category_edit'),
    url(r'^notice/category/add/$', 'manager.views_notice.add_category', name='notice_category_add'),

    # Lecture
    url(r'^lecture/?$', 'manager.views.lecturelist', name='lecturelist'),
    url(r'^lecture/dashboard/?$', 'manager.views.lecture_dashboard', name='lecture_dashboard'),
    url(r'^lecture/list$', 'manager.views.view_lecturelist', name='lecturelist_view'),
    url(r'^lecture/room/?$', 'manager.views.lectureroom', name='lectureroom'),
    url(r'^lecture/room/remove/?$', 'manager.views.lectureroom_remove', name='lectureroom_remove'),
    url(r'^lecture/block/?$', 'manager.views.lectureblock', name='lectureblock'),
    url(r'^lecture/block/new/?$', 'manager.views.lectureblock_new', name='lectureblock_new'),

    #임시. 나중에 바꿀것
    # url(r'^lecture/?$', 'manager.views.lecturelist', name='lectureblock'),

    url(r'^only_admin', 'manager.views.only_admin', name='only_admin'),
)