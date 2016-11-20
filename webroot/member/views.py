#-*- coding: utf-8 -*-
import hashlib
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from forms import AwardForm, CareerForm
from models import SomaUser
from models import Award, Career

# 멘티들의 정보에 접근할 수 있는 관리자 권한이 있는지 리턴
# 현재는 is_staff와 is_superuser만 접근가능
def is_admin(user):
    if user.is_staff == False and user.is_superuser == False:
        return False
    else:
        return True

@login_required
def profile(request, id=None):
    if id == None:
        user = request.user
    else:
        if is_admin(request.user):
            user = SomaUser.objects.get(id=id)
        else:
            return redirect('manager:only_admin')

    awards = Award.objects.filter(member=user).order_by('-date')
    careers = Career.objects.filter(member=user).order_by('-end_date')
    d = {
        'user': user,
        'awards': awards,
        'careers': careers,
    }

    return render_to_response('member/profile.html', d)

def edit_profile(request, id=None):
    if id == None:
        user = request.user
    else:
        user = SomaUser.objects.get(id=id)

def add_award(request):
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']

            award = Award(member=user, title=title, date=date, description=description)
            award.save()

            return redirect('member:profile')
        else:
            return render_to_response('member/add_award.html', {'form': form,}, RequestContext(request))    
    else:
        form = AwardForm()
        return render_to_response('member/add_award.html', {'form': form,}, RequestContext(request))

def delete_award(request, id):
    Award.objects.get(id=id).delete()
    return redirect('member:profile')

def delete_career(request, id):
    Career.objects.get(id=id).delete()
    return redirect('member:profile')

def add_career(request):
    if request.method == 'POST':
        form = CareerForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            description = form.cleaned_data['description']

            award = Career(member=user, title=title, start_date=start_date, end_date=end_date, description=description)
            award.save()

            # return HttpResponse(u'경력사항(' + title + u') 이 등록되었습니다')
            # redirect를 view로 하려면 어떻게 쓰는것이 맞는지?
            return redirect('member:profile')
        else:
            return render_to_response('member/add_career.html', {'form': form,}, RequestContext(request))    
    else:
        form = CareerForm()
        return render_to_response('member/add_career.html', {'form': form,}, RequestContext(request))


def check_id(request):
    print request
    print request.GET

    return HttpResponse(False)