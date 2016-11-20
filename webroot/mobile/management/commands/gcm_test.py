#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from document.models import Document

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from mobile.api import send_gcm

class Command(BaseCommand):

    def handle(self, *args, **options):
        print '-- GCM Send Test Start --'
        reg_id_list = [User.objects.get(username=u'leehanyeong').android_registration_id]
        data = {
            'document': Document.objects.get(id=1).get_document().json(),
        }
        print data
        send_gcm(reg_id_list, data)
        print '-- GCM Send Test End ----'