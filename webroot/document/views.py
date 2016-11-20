#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from datetime import datetime, time, timedelta

from project.models import Project, ProjectType

from document.models import Document, Sign
from document.models import DonationReceipt
from document.models import MentoringType, MentoringReport
from document.forms import MentoringReportForm, DonationReceiptForm

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta
from datetime import datetime, time, timedelta
from nptime import nptime

from somain.settings import MEDIA_ROOT, MEDIA_URL

# mktime 써보기
def get_time_seconds(time):
    hour = time.hour
    minute = time.minute
    second = time.second

    return (3600*hour + 60*minute + second)


def get_real_time(start_time, end_time):
    hour = end_time.hour - start_time.hour
    minute = end_time.minute - start_time.minute
    time = hour*60 + minute

    return time

def get_accept_time(start_time, end_time):
    start_second = get_time_seconds(start_time)
    end_second = get_time_seconds(end_time)

    total_second = end_second - start_second
    thirty_minute_number = total_second / 1800

    hour = 0
    minute = 0

    while thirty_minute_number > 1:
        thirty_minute_number = thirty_minute_number - 2
        hour = hour + 1

    minute = thirty_minute_number * 30

    time = hour*60 + minute

    return time

def get_strftime(minute):
    hour = 0
    while minute >= 60:
        hour = hour + 1
        minute = minute - 60

    return '%s:%s' % (str(hour).zfill(2), str(minute).zfill(2))


# 온라인 서류제출 메인
def index(request):
    user = request.user

    require_sign_documents = []
    docs = user.document_by_sign_user.filter(is_complete=False)
    require_submit_documents = user.document_by_sign_user.filter(is_complete=True).filter(is_submitted=False)
    recent_submit_documents = user.document_by_sign_user.filter(is_complete=True).filter(is_submitted=True).order_by('-submit_time')[:5]
    for doc in docs:
        if doc.sign_by_document.filter(user=user).exists():
            pass
        else:
            require_sign_documents.append(doc)
    d = {
        'user': user,
        'require_sign_documents': require_sign_documents,
        'require_submit_documents': require_submit_documents,
        'recent_submit_documents': recent_submit_documents,
    }

    return render_to_response('document/index.html', d, RequestContext(request))

def sign(request, document_id):
    user = request.user
    all_signed = True
    document = Document.objects.get(id=document_id).get_document()
    user_is_signed = document.sign_by_document.filter(user=user).exists()
    sign_users = document.sign_users.all()
    sign_infos = []

    # 서명해야할 사용자와 각 사용자의 서명여부 전달
    for sign_user in sign_users:
        sign_user_signed = document.sign_by_document.filter(user=sign_user).exists()
        if not sign_user_signed:
            all_signed = False

        sign_data = {
            'user': sign_user,
            'is_signed': document.sign_by_document.filter(user=sign_user).exists(),
            'all_signed': all_signed,
        }
        sign_infos.append(sign_data)

    # all_signed라면 document의 is_complete를 바꾸어준다
    if all_signed:
        document.is_complete = True
        document.save()


    # 서류 종류에 따라 다르게 데이터 전달
    if document.doc_title == u'멘토링 보고서':
        data = {
            u'구분': document.type,
            u'프로젝트': document.project,
            u'멘토링 날짜': document.date,
            u'장소': document.place,
            u'멘토링 주제': document.title,
            u'멘토링 내용': document.content,
        }
    elif document.doc_title == u'지출 계획서':
        pass

    # 전달할 데이터
    d = {
        'user': user,
        'user_is_signed': user_is_signed,
        'document': document,
        'sign_infos': sign_infos,
        'data': data,
    }

    # POST방식일 땐 서명정보를 생성 및 저장 후 페이지 로드
    if request.method == 'POST':
        Sign.objects.filter(user=request.user, document=document).delete()
        cur_sign = Sign(user=request.user, document=document)
        cur_sign.save()
        # 메시지 전달
        messages.add_message(request, messages.SUCCESS, document.doc_title)
        return redirect('document:sign', document_id)

    else:
        return render_to_response('document/sign.html', d, RequestContext(request))


def submit(request, document_id):
    user = request.user
    document = Document.objects.get(id=document_id)
    if document.is_complete == False:
        return HttpResponse('서명이 완료되지않음')

    try:
        document.is_submitted = True
        document.submit_time = datetime.today()
        document.submit_user = user
        document.save()
        messages.add_message(request, messages.SUCCESS, u'제출 완료')
        print u'제출완료'
    except:
        messages.add_message(request, messages.ERROR, u'제출에 실패')
        print u'제출실패'

    return redirect(request.META['HTTP_REFERER'])


def document_view(request, document_id):
    # print request
    user = request.user
    document = Document.objects.get(id=document_id).get_document()
    if document.doc_title == u'멘토링 보고서':
        return redirect('document:mentoring_report_view', document.id)
    elif document.doc_title == u'기부금 영수증':
        return redirect('document:donationreceipt_view', document.id)
    else:
        return HttpResponse(u'미지원 문서 뷰 타입입니다')


# 멘토만 가능, 작성 전 프로젝트를 선택하도록 함
def mentoring_report_write_choose(request):
    user = request.user
    manage_projects = user.project_by_mentor.filter(is_finished=False)
    projects = Project.objects.filter(is_finished=False)

    d = {
        'manage_projects': manage_projects,
        'projects': projects,
    }

    return render_to_response('document/mentoring_report_choose.html', d, RequestContext(request))


def get_timedelta(time):
    return timedelta(hours=time.hour, minutes=time.minute)

def get_timedelta_minus(time):
    return timedelta(hours=-time.hour, minutes=-time.minute)

# 멘토만 가능하도록 데코레이터
def mentoring_report_write(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        #form.mentees.queryset = User.objects.filter()
        form = MentoringReportForm(request.POST, initial={'project': project})

        if form.is_valid():
            print form.cleaned_data
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            #print form.cleaned_data['mentees']
            print type(start_time)
            print type(end_time)

            obj = form.save(commit=False)
            # 실제시간과 인정시간 입력
            #obj.real_time = end_time - relativedelta(hours=start_time.hour, minutes=start_time.minute)
            #obj.accept_time = end_time - relativedelta(hours=start_time.hour, minutes=start_time.minute)
            #obj.real_time = time(2,0)
            #obj.accept_time = time(2,0)
            obj.real_time = nptime(end_time.hour, end_time.minute) + timedelta(hours=-start_time.hour, minutes=-start_time.minute)
            obj.accept_time = nptime(end_time.hour, end_time.minute) + timedelta(hours=-start_time.hour, minutes=-start_time.minute)

            #print 'accept_time:', obj.accept_time
            #print 'obj.accept_time > nptime(4, 0):', obj.accept_time > nptime(4, 0)
            if obj.accept_time > nptime(4, 0):
                obj.accept_time = nptime(4, 0)
                print obj.accept_time

            # 프로젝트지정
            #type(form.cleaned_data['project_id'])
            #project_id = int(form.cleaned_data['project_id'])
            #type(project_id)
            project = Project.objects.get(id=project_id)
            obj.project = project

            #print 'debug1'
            # 제출기한시간 입력
            d1 = datetime.today()
            d2 = d1.replace(day=d1.day+1, hour=18, minute=0, second=0)
            obj.deadline = d2
            #print 'debug2'
            #print obj

            obj.save()
            #print type(obj)
            #print obj.sign_users
            #print 'debug3'

            # 유저 멘토여부 검사
            mentor = request.user
            if mentor.type.title != u'멘토':
                return HttpResponse(mentor + u'는 멘토가 아닙니다')
            else:
                obj.mentor = mentor

            ''' 아래 2개 한번에 실행 '''
            ''' 참여 연수생 정보를 다시 저장 '''
            ''' 서명이 필요한 사용자에 프로젝트의 멘토와 참여 멘티들을 추가해서 저장한다 '''
            #print form.cleaned_data['project'].mentor
            #print type(form.cleaned_data['project'].mentor)
            #mentor_id = form.cleaned_data['mentor_id']
            obj.sign_users.add(mentor)
            for mentee in form.cleaned_data['mentees'].all():
                obj.mentees.add(mentee)
                obj.sign_users.add(mentee)
            obj.save()

            # GCM 전송
            from mobile.api import send_gcm
            reg_id_list = [user.android_registration_id for user in obj.sign_users.all()]
            data = {
                'document': obj.json(),
            }
            send_gcm(reg_id_list, data)

            return redirect('document:index')
        else:
            return render_to_response('document/mentoring_report_write.html', {'form': form,}, RequestContext(request))
    else:
        initial_data = {
            'type': MentoringType.objects.get(title=u'정규'),
            'project': project,
        }
        form = MentoringReportForm(initial=initial_data)
        form.fields['type'].empty_label = None
        #form.fields['project'].queryset = Project.objects.filter(id=project_id)
        #form.fields['cooperation_mentor'].queryset = User.objects.filter(type__title=u'멘토')
        form.fields['mentees'].help_text = None
        form.fields['mentees'].queryset = project.mentees.all()
        # form.project.queryset = project

        dict = {
            'form': form,
            'project': project,
            'mentor': request.user,
        }

        return render_to_response('document/mentoring_report_write.html', dict, RequestContext(request))

def mentoring_report_list(request):
    user = request.user
    # user = User.objects.get(username='leehanyeong')
    projects = []
    if user.type.title == u'멘티':
        projects = user.project_by_mentees.all()
    elif user.type.title == u'멘토':
        projects = user.project_by_mentor.all()

    d = {}

    d['projects'] = projects

    return render_to_response('document/mentoring_report_list.html', d, RequestContext(request))

def mentoring_report_view(request, document_id):
    try:
        cur_report = Document.objects.get(id=document_id).get_document()
    except:
        return HttpResponse('No Report')

    project = cur_report.project
    reports = MentoringReport.objects.filter(project=project)
    month = cur_report.date.month

    user_info = {}
    users = cur_report.mentees.all()
    for i in range(len(users)):
        user = users[i]
        key = u'%s%d' % (u'user', i)
        if user.sign_by_user.filter(document=cur_report).exists():
            value = {
                'is_signed': True,
                'sign': Sign.objects.get(document=cur_report, user=user)
            }
        else:
            value = {
                'is_signed': False,
            }

        user_info[key] = value


    d = {
        'project': project,
        'reports': reports,
        'cur_report': cur_report,
        'month': month,
        'media_url': MEDIA_URL,
        'user_info': user_info,
    }

    return render_to_response('document/mentoring_report.html', d, RequestContext(request))



''' DonationReceipt '''
def donationreceipt_view(request, document_id):
    try:
        cur_receipt = Document.objects.get(id=document_id).get_document()
    except:
        return HttpResponse('No Report')

    receipts = DonationReceipt.objects.filter(sign_users=request.user)
    print 'document_id', document_id
    print 'user', request.user
    if Sign.objects.filter(document=Document.objects.get(id=document_id)).filter(user=request.user).exists():
        print 'is_signed'
        cur_sign = Sign.objects.get(document=Document.objects.get(id=document_id), user=request.user)
        is_signed = True
    else:
        print 'is_not_signed'
        cur_sign = None
        is_signed = False

    d = {
        'media_url': MEDIA_URL,
        'cur_receipt': cur_receipt,
        'cur_sign': cur_sign,
        'is_signed': is_signed,
        'receipts': receipts,
    }
    print 'receipts:', receipts

    return render_to_response('document/donationreceipt.html', d, RequestContext(request))

def donationreceipt_write(request, document_id):
    user = request.user
    donationreceipt = DonationReceipt.objects.get(id=document_id)

    if request.method == 'POST':
        form = DonationReceiptForm(request.POST, initial={})

        if form.is_valid():
            print form.cleaned_data
            obj = form.save(commit=False)
            obj.save()
            return redirect('document:index')
        else:
            return render('document/donationreceipt_write.html', {'form': form}, RequestContext(request))
    else:
        form = DonationReceiptForm
        dict = {
            'form': form,
        }
        return render_to_response('document/donationreceipt_write.html', dict, RequestContext(request))