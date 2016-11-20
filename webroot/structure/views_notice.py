#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.shortcuts import HttpResponse
from django.template import RequestContext

from structure.models import Notice, NoticeCategory
from structure.forms_notice import  NoticeForm

def list(request):
    user = request.user

    notices = Notice.objects.all().order_by('-id')

    d = {
        'user': user,
        'notices': notices,
    }
    return render_to_response('notice/list.html', d, RequestContext(request))

def detail(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    prev_notice = Notice.objects.filter(id__gt=notice.id).order_by('id')[0:1]
    next_notice = Notice.objects.filter(id__lt=notice.id).order_by('-id')[0:1]

    if len(prev_notice) > 0:
        prev_notice = prev_notice[0]
    if len(next_notice) > 0:
        next_notice = next_notice[0]

    d = {
        'notice': notice,
        'prev': prev_notice,
        'next': next_notice,
    }

    return render_to_response('notice/detail.html', d, RequestContext(request))


def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('notice:list')
        else:
            return HttpResponse('invalid form data')
    else:
        form = NoticeForm()
        dict = {
            'form': form,
        }

        return render_to_response('notice/add.html', dict, RequestContext(request))
