#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

import os.path
import hashlib
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

TYPE_MAIL_STATUS = (
    ('1', '발송대기'),
    ('2', '발송중'),
    ('3', '발송완료'),
    ('4', '발송실패'),
)

class MailContent(models.Model):
    title = models.CharField('제목', max_length=80)
    content = models.TextField('본문')
    attachment = models.CommaSeparatedIntegerField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

class Mail(models.Model):
    mail_from = models.ForeignKey(User, related_name='+')
    mail_to = models.ForeignKey(User, related_name='+')
    mail = models.ForeignKey(MailContent)
    status = models.CharField('발송상태', max_length=1, choices=TYPE_MAIL_STATUS, db_index=True)
    send_at = models.DateTimeField(auto_now=True) # 전송이 완료되었을 때 표시
    read = models.BooleanField('읽음확인', default=False)
    read_at = models.DateTimeField(auto_now=True) # 읽음 확인이 true 일 때 표시
    created_at = models.DateTimeField(auto_now_add=True)

class MailAttachment(models.Model):
    file = models.FileField(upload_to='mail') # mail attachment
    md5sum = models.CharField(max_length=36, unique=True) # Unique Key
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def down_url(self):
        return 'http://' + settings.HOST + '/mail/attachment/' + self.md5sum

    def filename(self):
        return os.path.basename(self.file.name)

    def filesize(self):
        return self.file.size

    def strfsize(self):
        num = self.file.size
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()

            if MailAttachment.objects.filter(md5sum=self.md5sum).exists():
                return MailAttachment.objects.get(md5sum=self.md5sum)

            self.expires_at = (datetime.now() + timedelta(hours=24 * settings.EMAIL_ATTACHMENT_EXPIRES))
        super(MailAttachment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(MailAttachment, self).delete(*args, **kwargs)

