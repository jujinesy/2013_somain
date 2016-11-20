from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # default admin
    url(r'^django_admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^django_admin/', include(admin.site.urls)),

    # structure
    url(r'^$', 'structure.views.main'),
    # url(r'^edit_profile/$', 'structure.views.edit_profile', name='edit_profile'),
    url(r'^check_id/$', 'member.views.check_id', name='check_id'),

    # django-registration
    url(r'^accounts/', include('registration.backends.default.urls')),

    # manager
    url(r'^admin/', include('manager.urls', namespace='manager')),

    # member
    url(r'^member/', include('member.urls', namespace='member')),
    
    # korzip / lecture / mail
    url(r'^korzip/', include('korzip.urls', namespace='korzip')),
    url(r'^lecture/', include('lectureroom.urls', namespace='lecture')),
    url(r'^mail/', include('mail.urls', namespace='mail')),

    # Test
    url(r'^send_mail_test/', 'structure.mail.send_staff_view', name='send_staff'),

    # document
    url(r'^document/', include('document.urls', namespace='document')),

    # Notice
    url(r'^notice/', include('structure.urls_notice', namespace='notice')),

    # Mobile API
    url(r'^mobile/', include('mobile.urls', namespace='mobile')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
