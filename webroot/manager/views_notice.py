#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.shortcuts import HttpResponse
from django.template import RequestContext

from structure.models import Notice, NoticeCategory
from structure.forms_notice import  NoticeForm, NoticeCategoryForm

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

def list(request):
    user = request.user

    notices = Notice.objects.all()
    categories = NoticeCategory.objects.all()

    d = {
        'active_li': 'list',
        'user': user,
        'notices': notices,
        'categories': categories,
    }
    return render_to_response('manager/notice/list.html', d, RequestContext(request))

def detail(request, notice_id):
    notice = Notice.objects.get(id=notice_id)

    d = {
        'active_li': 'detail',
        'notice': notice,
    }
    return render_to_response('manager/notice/detail.html', d, RequestContext(request))


def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)

        if form.is_valid():
            form.save()

            # GCM 전송
            from mobile.api import send_gcm_simple
            users = User.objects.filter(type__title=u'멘티')
            reg_id_list = [user.android_registration_id for user in users]
            data = {
                'title': form.cleaned_data['title']
            }
            send_gcm_simple(reg_id_list, data)

            return redirect('manager:notice')
        else:
            return HttpResponse('invalid form data')
    else:
        form = NoticeForm()
        dict = {
            'active_li': 'add',
            'form': form,
        }
        return render_to_response('manager/notice/add.html', dict, RequestContext(request))

def edit_notice(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('manager:notice')
        else:
            return HttpResponse('invalid form data')
    else:
        form = NoticeForm(instance=notice)
        dict = {
            'active_li': 'edit',
            'form': form,
        }
        return render_to_response('manager/notice/edit.html', dict, RequestContext(request))

def category_list(request):
    categories = NoticeCategory.objects.all()

    d = {
        'active_li': 'category_list',
        'categories': categories,
    }

    return render_to_response('manager/notice/category_list.html', d, RequestContext(request))

def category_detail(request, category_id):
    category = NoticeCategory.objects.get(id=category_id)

    d = {
        'active_li': 'category_detail',
        'category': category,
    }

    return render_to_response('manager/notice/category_detail.html', d, RequestContext(request))

def add_category(request):
    if request.method == 'POST':
        form = NoticeCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manager:notice_category')
        else:
            return HttpResponse('invalid form data')
    else:
        form = NoticeCategoryForm()
        dict = {
            'active_li': 'category_add',
            'form': form,
        }

        return render_to_response('manager/notice/category_add.html', dict, RequestContext(request))

def edit_category(request, category_id):
    category = NoticeCategory.objects.get(id=category_id)
    if request.method == 'POST':
        form = NoticeCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manager:notice_category')
        else:
            return HttpResponse('invalid form data')
    else:
        form = NoticeCategoryForm(instance=category)
        dict = {
            'active_li': 'category_edit',
            'form': form,
        }
        return render_to_response('manager/notice/category_edit.html', dict, RequestContext(request))