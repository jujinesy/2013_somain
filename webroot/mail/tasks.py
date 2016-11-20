#-*- coding: utf-8 -*-
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.shortcuts import render
import smtplib

from .models import Mail, MailContent, MailAttachment

# 매 분마다 실행되는 메일발송 작업
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def mail_task():
    def strfsize(num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    # 발송이 진행중인 메일작업이 있으면 건너뛴다
    if Mail.objects.filter(status="2").exists():
        return

    # 보낼 메일이 있는지 확인
    if not Mail.objects.filter(status="1").exists():
        return

    # 보낼 메일을 가져온다
    mail = Mail.objects.filter(status="1").order_by('created_at')[0]
    cont = mail.mail

    mail.save()

    content = cont.content
    file_list = []
    size = 0
    if cont.attachment:
        files = cont.attachment.split(',')
        for file_id in files:
            file = MailAttachment.objects.get(id=file_id)
            if file:
                #print file.file.name.replace('mail/', ''), file.file.size, file.strfsize()
                size += file.file.size
                file_list.append(file)

        if len(file_list) > 0:
            file_expires = "%s ~ %s" % ( cont.created_at.strftime('%Y-%m-%d'), (cont.created_at + timedelta(hours=24 * settings.EMAIL_ATTACHMENT_EXPIRES)).strftime('%Y-%m-%d') )

            t = get_template('mail/mail_file.html')
            file_html = t.render(Context({ 'file_count': len(file_list), 'file_size': strfsize(size), 'files': file_list, 'file_expires': file_expires }))
            content = file_html + content

        content = ( "<img src=\"http://%s/mail/check/%s/%s\" alt=\"\">" % ( settings.HOST, mail.mail_to.id, mail.id ) ) + content

    # 메일 발송처리
    try:
        mail.status = "2" # 발송중
        #send_mail(cont.title, content, mail.mail_from.email, [ mail.mail_to.email ], fail_silently=False)
        msg = EmailMultiAlternatives(cont.title, content, mail.mail_from.email, [ mail.mail_to.email ])
        msg.attach_alternative(content, "text/html")
        msg.send()
        mail.status = "3" # 발송 완료
        mail.save()
    except smtplib.SMTPException:
        mail.status = "4" # 발송 실패
        mail.save()
        return

# 1일마다 실행되는 작업: 메일 첨부파일 기간확인 후 기간 지난건 삭제
@periodic_task(run_every=crontab(hour="0", minute="*", day_of_week="*"))
def attachment_task():
    today = datetime.now()
    #files = #MailAttachment.objects.filter(expires_at__gte=today)

    #for files in file:
    #    file.delete()

    return
