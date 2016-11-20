#-*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.conf import settings
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper

from manager.decorator import staff_login_required as staff

from .models import Mail, MailAttachment, MailContent
from .forms import MailForm

from datetime import datetime

import mimetypes
import os

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

@staff
def check(request, user='', id=''):
    if not request.META.HTTP_REFERER:
        raise Http404

    if not User.objects.filter(id=user).exists():
        raise Http404

    if not Mail.objects.filter(id=id, mail_to=user).exists():
        raise Http404

    mail = Mail.objects.filter(id=id, mail_to=user)
    mail.read = True
    mail.read_at = datetime.now()
    mail.save()

    return HttpResponse('')

def attachment(request, hash=''):
    if not MailAttachment.objects.filter(md5sum=hash).exists():
        raise Http404 # 파일이 없을 경우 404 오류 반환

    file = MailAttachment.objects.get(md5sum=hash)
    fpath = file.file.path
    content_type = mimetypes.guess_type(fpath)[0]

    if settings.DEBUG == True:
        wrapper = FileWrapper(open(fpath))
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(fpath)
        response['Content-Disposition'] = "attachment; filename=%s" % file.filename()
        return response
    else:
        response = HttpResponse(content_type=content_type)
        response['Content-Length'] = os.path.getsize(fpath)
        response['Content-Disposition'] = "attachment; filename=%s" % file.filename()
        response['X-Accel-Redirect'] = fpath
        return response

@staff
def write(request):
    if request.method == 'POST' and request.POST.get('type', '') == 'write':
        return write_post(request)

    d = {
        'user': request.user,
        'mail_to': [],
        'form': MailForm(),
    }

    mail_to = request.REQUEST.get('to', '')
    mail_to_filter = []
    mail_to_user = []
    if mail_to != '':
        for id in mail_to.split(','):
            user = User.objects.get(id=id)
            if user:
                mail_to_filter.append(id)
                mail_to_user.append(user)

        d['form'] = MailForm(initial={ 'mail_to': ','.join(mail_to_filter) })
        d['users'] = mail_to_user

    if len(mail_to_filter) == 0:
        return HttpResponse('<script> alert("메일 수신자를 선택해주세요."); window.close(); </script>')

    return render_to_response('mail/write.html', d, RequestContext(request))

# post request
def write_post(request):
    mail_form = MailForm(request.POST)

    if not mail_form.is_valid():
        msg = ''
        for error in mail_form.errors:
            if error == 'title':
                msg = '메일 제목을 입력해주세요.'
            elif error == 'content':
                msg = '메일 내용을 입력해주세요.'
            elif error == 'mail_to':
                msg = '메일 수신자가 없습니다.'
        return HttpResponse('<script> alert("' + msg + '"); history.go(-1) </script>')

    # 첨부파일 처리
    attachments = request.FILES.getlist('file[]')
    files = []
    files_id = []
    for file in attachments:
        f = MailAttachment.objects.create(
            file=file,
            user=request.user
        )
        f = f.save()
        files.append(f)
        files_id.append(str(f.id))

    # 메일 콘텐츠 처리
    title = mail_form.cleaned_data['title']
    content = mail_form.cleaned_data['content']

    if MailContent.objects.filter(title=title).exists():
        return HttpResponse('<script> alert("같은 제목을 가진 메일이 있습니다."); history.go(-1) </script>')

    mail_content = MailContent.objects.create(
        title=title,
        content=content,
        attachment=','.join(files_id)
    )
    mail_content.save()

    # 메일 큐에 넣기
    mail_to = mail_form.cleaned_data['mail_to'].split(',')
    mails = []
    mails_id = []
    for id in mail_to:
        mail = Mail.objects.create(
            mail_from=request.user,
            mail_to=User.objects.get(id=id),
            mail=mail_content,
            status='1'
        )
        mail.save()
        mails.append(mail)
        mails_id.append(mail.id)

    return HttpResponse('<script> alert("메일 발송처리가 완료되었습니다. 발송 상태는 관리자페이지에서 확인하실 수 있습니다."); window.close() </script>')