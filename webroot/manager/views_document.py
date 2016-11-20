#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# decorator
from django.contrib.auth.decorators import login_required

# python library
from datetime import datetime
from dateutil.relativedelta import relativedelta

# member 모델
from member.models import SomaUser
from member.models import Award, Career

# settings.py
from somain.settings import MEDIA_ROOT, MEDIA_URL

# manager 함수
from manager.models import modify_permission, modify_step

# Excel
from tempfile import TemporaryFile
from xlwt import Workbook

# LectureRoom 모델
from lectureroom.models import LectureRoom, LectureBlock, Lecture

# Proejct 모델
from project.models import *

# Document 모델
from document.models import *

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Log
from log.models import create_log
from log.models import Type as Log_Type

# decorator
from manager.decorator import staff_login_required

# custom functions
from manager.functions import get_strftime

# views_document_mentoringreport
from manager.views_document_mentoringreport import mentoringreport_mentor_list
from manager.views_document_mentoringreport import mentoringreport_mentee_list
from manager.views_document_mentoringreport import mentoringreport_project_list
from manager.views_document_mentoringreport import mentoringreport_total_list

# from manager.views_document_mentoringreport import mentoringreport_period

'''
type1 : total(전체), mentor(멘토별), mentee(멘티별), project(프로젝트별)로 구분
type2
    total : monthly, full
    mentor : monthly, step, full
    mentee : monthly, step, full
    project : monthly, step, full
'''
def index(request):
    return redirect('manager:document_mentoringreport')


def mentoringreport(request):
    if request.method == 'POST':
        query_dict = request.POST
        if query_dict.has_key('type1'):
            return mentoringreport_type1(request)
        else:
            return HttpResponse('no')
    else:
        dict = {
            'type1': 'total',
            'type2': 'monthly',
        }

        #query_dict['type1'] = 'total',
        #return render_to_response('manager/document/mentoringreport/total_list_monthly.html', dict, RequestContext(request))
        #request.POST['type1'] = 'total'
        #request.POST['type2'] = 'monthly'
        return mentoringreport_total_list(request)

def mentoringreport_type1(request):
    query_dict = request.POST
    type1 = query_dict['type1']
    type2 = query_dict['type2']
    print 'mentoringreport_type1, type1:', type1, 'type2:', type2
    #print query_dict

    # 단계 또는 기간 선택일 경우 선택화면으로 바로 이동
    if type2 == 'step':
        return mentoringreport_select_step(request)
    elif type2 == 'period':
        if not query_dict.has_key('period_selected'):
            return mentoringreport_select_period(request)
        else:
            print 'mentoringreport_type1, type2:', type2, 'period_selected:true'

    if type1 == 'total':
        return mentoringreport_total_list(request)
    elif type1 == 'mentor':
        return mentoringreport_mentor_list(request)
    elif type1 == 'mentee':
        return mentoringreport_mentee_list(request)
    elif type1 == 'project':
        return mentoringreport_project_list(request)
    else:
        return HttpResponse('type1 no matching(' + type1 + ')')


def donationreceipt(request):
    if request.method == 'POST':
        query_dict = request.POST

        if query_dict.has_key('type1'):
            return mentoringreport_type1(request)
        else:
            return HttpResponse('no')
    else:
        dict = {
            'type1': 'total',
            'type2': 'monthly',
        }

        #query_dict['type1'] = 'total',
        #return render_to_response('manager/document/mentoringreport/total_list_monthly.html', dict, RequestContext(request))
        #request.POST['type1'] = 'total'
        #request.POST['type2'] = 'monthly'
        return mentoringreport_total_list(request)

# def mentoringreport_total(request):
#     query_dict = request.POST
#     if query_dict.has_key('type2'):
#         type2 = query_dict['type2']
#         if type2 == 'monthly' or type2 == 'monthly2':
#             return mentoringreport_total_list(request)
#         elif type2 == 'full':
#             return mentoringreport_total_full(request)
#         elif type2 == 'step':
#             return mentoringreport_select_step(request)
#         elif type2 == 'period':
#             return mentoringreport_select_period(request)
#         else:
#             return HttpResponse('total/type2 no matching')
#     else:
#         return HttpResponse('total/no type2')

# def mentoringreport_mentor(request):
#     query_dict = request.POST
#     print query_dict
#     if query_dict.has_key('type2'):
#         type2 = query_dict['type2']
#         if type2 == 'monthly' or type2 == 'monthly2':
#             return mentoringreport_mentor_list(request)
#         elif type2 == 'total':
#             pass
#         elif type2 == 'step':
#             return mentoringreport_select_step(request)
#         elif type2 == 'period':
#             return mentoringreport_select_period(request)
#         else:
#             return HttpResponse('mentor/type2 no matching')
#     else:
#         return HttpResponse('mentor/no type2')

# def mentoringreport_mentee(request):
#     query_dict = request.POST
#     if query_dict.has_key('type2'):
#         type2 = query_dict['type2']
#         if type2 == 'monthly' or type2 == 'monthly2':
#             return mentoringreport_mentee_list(request)
#         elif type2 == 'total':
#             pass
#         elif type2 == 'step':
#             return mentoringreport_select_step(request)
#         elif type2 == 'period':
#             return mentoringreport_select_period(request)
#         else:
#             return HttpResponse('mentee/type2 no matching')
#     else:
#         return HttpResponse('mentee/no type2')

# def mentoringreport_project(request):
#     query_dict = request.POST
#     if query_dict.has_key('type2'):
#         type2 = query_dict['type2']
#         if type2 == 'monthly' or type2 == 'monthly2':
#             return mentoringreport_project_list(request)
#         elif type2 == 'total':
#             pass
#         elif type2 == 'step':
#             return mentoringreport_select_step(request)
#         elif type2 == 'period':
#             return mentoringreport_select_period(request)
#         else:
#             return HttpResponse('project/type2 no matching')
#     else:
#         return HttpResponse('project/no type2')    


def mentoringreport_select_step(request):
    return HttpResponse('select step')


# 기간 선택 화면
def mentoringreport_select_period(request):
    query_dict = request.POST
    # 기간 선택 후 이동했을 경우 결과화면 이동 분기로 리턴(아래 mentoringreport_period 뷰)
    #if query_dict.has_key('period_selected'):
    #    #print 'has_period_selected:', query_dict['period_selected']
    #    return mentoringreport_period(request)

    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    type1 = query_dict['type1']
    type2 = query_dict['type2']
    type1_text = ''

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'type1': type1,
        'type2': type2,
    }
    if type1 == 'mentor':
        if query_dict.has_key('mentor'):
            ''' 특정 멘토 기간 검색일 경우 월별/단계별 시 사용할 mentor정보 전달, 템플릿에서 사용 '''
            mentor = User.objects.get(username=query_dict['mentor'])
            type1_text = mentor.last_name + mentor.first_name + u' 멘토 기간 검색'
            mentor_dict = { 'mentor': mentor, }
            d['mentor_info'] = mentor_dict
        else:
            type1_text = u'멘토 기간 검색'
    elif type1 == 'mentee':
        if query_dict.has_key('mentee'):
            mentee = User.objects.get(username=query_dict['mentee'])
            type1_text = mentee.last_name + mentee.first_name + u' 멘티 기간 검색'
            d['mentee'] = mentee
        else:
            type1_text = u'멘티 기간 검색'
    elif type1 == 'project':
        if query_dict.has_key('project_id'):
            project = Project.objects.get(id=int(query_dict['project_id']))
            type1_text = project.title + u' 프로젝트 기간 검색'
        else:
            type1_text = u'프로젝트 기간 검색'
    elif type1 == 'total':
        type1_text = u'전체 멘토링보고서 기간 검색'

    d['type1_text'] = type1_text

    return render_to_response('manager/document/mentoringreport/select_period.html', d, RequestContext(request))






def mentoring_report(request, type1):
    if type1 == 'mentor':
        return redirect('manager:document_mentoring_report_mentor', 'monthly')
    elif type1 == 'mentee':
        return redirect('manager:document_mentoring_report_mentee', 'monthly')
    elif type1 == 'project':
        return redirect('manager:document_mentoring_report_project')
    elif type1 == 'total':
        return redirect('manager:document_mentoring_report_total')
    else:
        return HttpResponse('No Matching')

def mentoring_report_total(request, type2):
    if type2 == 'monthly':
        cur_time = datetime.today()
        return redirect('manager:document_mentoring_report_total_monthly', cur_time.year, cur_time.month)
    elif type2 == 'full':
        return redirect('manager:document_mentoring_report_total_full')



def mentoring_report_total_full(request):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentors = User.objects.filter(type__title=u'멘토')

    mentor_info_list = []
    for mentor in mentors:
        projects = Project.objects.filter(mentor=mentor)

        project_info_list = []
        total_count = 0
        total_real_time_minute = 0
        total_accept_time_minute = 0
        for project in projects:
            mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True)
            
            project_real_time_minute = 0
            project_accept_time_minute = 0
            for mentoring_report in mentoring_reports:
                project_real_time_minute = project_real_time_minute + mentoring_report.real_time
                project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time
                total_real_time_minute = total_real_time_minute + mentoring_report.real_time
                total_accept_time_minute = total_accept_time_minute + mentoring_report.accept_time
                total_count = total_count + 1

            project_dict = {
                'project': project,
                'mentoring_reports': mentoring_reports,
                'project_real_time_minute' : project_real_time_minute,
                'project_accept_time_minute' : project_accept_time_minute,
                'project_real_time' : get_strftime(project_real_time_minute),
                'project_accept_time' : get_strftime(project_accept_time_minute),
            }
            project_info_list.append(project_dict)

        mentor_dict = {
            'mentor': mentor,
            'project_info_list': project_info_list,
            'total_real_time_minute': total_real_time_minute,
            'total_accept_time_minute': total_accept_time_minute,
            'total_real_time' : get_strftime(total_real_time_minute),
            'total_accept_time' : get_strftime(total_accept_time_minute),
            'total_count': total_count,
        }
        mentor_info_list.append(mentor_dict)

    
    mentees = User.objects.filter(type__title=u'멘티')

    mentee_info_list = []
    for mentee in mentees:
        project = Project.objects.filter(is_finished=False).get(mentees=mentee)
        mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True).filter(mentees=mentee)

        project_real_time_minute = 0
        project_accept_time_minute = 0
        for mentoring_report in mentoring_reports:
            project_real_time_minute = project_real_time_minute + mentoring_report.real_time
            project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time

        mentee_dict = {
            'mentee': mentee,
            'project': project,
            'project_real_time': get_strftime(project_real_time_minute),
            'project_accept_time': get_strftime(project_accept_time_minute),
            'mentoring_reports': mentoring_reports,
        }

        mentee_info_list.append(mentee_dict)

        mentoring_report_full = MentoringReport.objects.filter(date__year=year).filter(date__month=month)

        d = {
            'title': title,
            'subtitle': subtitle,
            'active_li': active_li,

            'mentee_info_list': mentee_info_list,
            'mentor_info_list': mentor_info_list,
            'mentoring_report_full': mentoring_report_full,
        }

    return render_to_response('manager/document_mentoring_report_total.html', d, RequestContext(request))

def mentoring_report_mentor(request, type2):
    if type2 == 'monthly':
        cur_time = datetime.today()
        return redirect('manager:document_mentoring_report_mentor_monthly', cur_time.year, cur_time.month)
    else:
        return HttpResponse('No view')

def mentoring_report_mentor_monthly(request, year, month):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentors = User.objects.filter(type__title=u'멘토')

    mentor_info_list = []
    for mentor in mentors:
        projects = Project.objects.filter(mentor=mentor)

        project_info_list = []
        total_count = 0
        total_real_time_minute = 0
        total_accept_time_minute = 0
        for project in projects:
            mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True).filter(date__year=year).filter(date__month=month)
            
            project_real_time_minute = 0
            project_accept_time_minute = 0
            for mentoring_report in mentoring_reports:
                project_real_time_minute = project_real_time_minute + mentoring_report.real_time
                project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time
                total_real_time_minute = total_real_time_minute + mentoring_report.real_time
                total_accept_time_minute = total_accept_time_minute + mentoring_report.accept_time
                total_count = total_count + 1

            project_dict = {
                'project': project,
                'mentoring_reports': mentoring_reports,
                'project_real_time_minute' : project_real_time_minute,
                'project_accept_time_minute' : project_accept_time_minute,
                'project_real_time' : get_strftime(project_real_time_minute),
                'project_accept_time' : get_strftime(project_accept_time_minute),
            }
            project_info_list.append(project_dict)

        mentor_dict = {
            'mentor': mentor,
            'project_info_list': project_info_list,
            'total_real_time_minute': total_real_time_minute,
            'total_accept_time_minute': total_accept_time_minute,
            'total_real_time' : get_strftime(total_real_time_minute),
            'total_accept_time' : get_strftime(total_accept_time_minute),
            'total_count': total_count,
        }
        mentor_info_list.append(mentor_dict)

    print type(year)
    print type(month)
    cur_time = datetime.today().replace(year=int(year), month=int(month))
    prev_month_time = cur_time + relativedelta(months = -1)
    next_month_time = cur_time + relativedelta(months = +1)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentor_info_list': mentor_info_list,
        'year': year,
        'month': month,

        'prev_year': prev_month_time.year,
        'prev_month': prev_month_time.month,
        'next_year': next_month_time.year,
        'next_month': next_month_time.month,
    }

    return render_to_response('manager/document_mentoring_report_mentor_monthly.html', d, RequestContext(request))

def mentoring_report_mentor_monthly_detail(request, year, month, mentor_username):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentor = User.objects.get(username=mentor_username)
    projects = Project.objects.filter(mentor=mentor)

    project_info_list = []
    total_count = 0
    total_real_time_minute = 0
    total_accept_time_minute = 0
    for project in projects:
        mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True).filter(date__year=year).filter(date__month=month)

        project_real_time_minute = 0
        project_accept_time_minute = 0
        for mentoring_report in mentoring_reports:
            project_real_time_minute = project_real_time_minute + mentoring_report.real_time
            project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time
            total_real_time_minute = total_real_time_minute + mentoring_report.real_time
            total_accept_time_minute = total_accept_time_minute + mentoring_report.accept_time
            total_count = total_count + 1

        project_dict = {
            'project': project,
            'mentoring_reports': mentoring_reports,
            'project_real_time_minute' : project_real_time_minute,
            'project_accept_time_minute' : project_accept_time_minute,
            'project_real_time' : get_strftime(project_real_time_minute),
            'project_accept_time' : get_strftime(project_accept_time_minute),
        }
        project_info_list.append(project_dict)

    mentor_info = {
        'mentor': mentor,
        'project_info_list': project_info_list,
        'total_real_time_minute': total_real_time_minute,
        'total_accept_time_minute': total_accept_time_minute,
        'total_real_time' : get_strftime(total_real_time_minute),
        'total_accept_time' : get_strftime(total_accept_time_minute),
        'total_count': total_count,
    }

    cur_time = datetime.today().replace(year=int(year), month=int(month))
    prev_month_time = cur_time + relativedelta(months = -1)
    next_month_time = cur_time + relativedelta(months = +1)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentor_info': mentor_info,
        'year': year,
        'month': month,

        'prev_year': prev_month_time.year,
        'prev_month': prev_month_time.month,
        'next_year': next_month_time.year,
        'next_month': next_month_time.month,
    }

    return render_to_response('manager/document_mentoring_report_mentor_monthly_detail.html', d, RequestContext(request))


def mentoring_report_mentee(request, type2):
    if type2 == 'monthly':
        cur_time = datetime.today()
        return redirect('manager:document_mentoring_report_mentee_monthly', cur_time.year, cur_time.month)
    else:
        return HttpResponse('No view')

def mentoring_report_mentee_monthly(request, year, month):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentees = User.objects.filter(type__title=u'멘티')

    mentee_info_list = []
    for mentee in mentees:
        project = Project.objects.filter(is_finished=False).get(mentees=mentee)
        mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True).filter(mentees=mentee).filter(date__year=year).filter(date__month=month)

        project_real_time_minute = 0
        project_accept_time_minute = 0
        for mentoring_report in mentoring_reports:
            project_real_time_minute = project_real_time_minute + mentoring_report.real_time
            project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time

        mentee_dict = {
            'mentee': mentee,
            'project': project,
            'project_real_time': get_strftime(project_real_time_minute),
            'project_accept_time': get_strftime(project_accept_time_minute),
            'mentoring_reports': mentoring_reports,
        }

        mentee_info_list.append(mentee_dict)

    cur_time = datetime.today().replace(year=int(year), month=int(month))
    prev_month_time = cur_time + relativedelta(months = -1)
    next_month_time = cur_time + relativedelta(months = +1)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentee_info_list': mentee_info_list,
        'year': year,
        'month': month,

        'prev_year': prev_month_time.year,
        'prev_month': prev_month_time.month,
        'next_year': next_month_time.year,
        'next_month': next_month_time.month,
    }

    return render_to_response('manager/document_mentoring_report_mentee_monthly.html', d, RequestContext(request))

def mentoring_report_mentee_full(request):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentees = User.objects.filter(type__title=u'멘티')

    mentee_info_list = []
    for mentee in mentees:
        project = Project.objects.filter(is_finished=False).get(mentees=mentee)
        mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True).filter(mentees=mentee)

        project_real_time_minute = 0
        project_accept_time_minute = 0
        for mentoring_report in mentoring_reports:
            project_real_time_minute = project_real_time_minute + mentoring_report.real_time
            project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time

        mentee_dict = {
            'mentee': mentee,
            'project': project,
            'project_real_time': get_strftime(project_real_time_minute),
            'project_accept_time': get_strftime(project_accept_time_minute),
            'mentoring_reports': mentoring_reports,
        }

        mentee_info_list.append(mentee_dict)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentee_info_list': mentee_info_list,
    }

    return render_to_response('manager/document_mentoring_report_mentee_full.html', d, RequestContext(request))

def mentoring_report_mentee_monthly_detail(request, year, month, mentee_username):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentor = User.objects.get(username=mentor_username)
    projects = Project.objects.filter(mentor=mentor)

    project_info_list = []
    total_count = 0
    total_real_time_minute = 0
    total_accept_time_minute = 0
    for project in projects:
        mentoring_reports = MentoringReport.objects.filter(project=project).filter(is_submitted=True).filter(date__year=year).filter(date__month=month)

        project_real_time_minute = 0
        project_accept_time_minute = 0
        for mentoring_report in mentoring_reports:
            project_real_time_minute = project_real_time_minute + mentoring_report.real_time
            project_accept_time_minute = project_accept_time_minute + mentoring_report.accept_time
            total_real_time_minute = total_real_time_minute + mentoring_report.real_time
            total_accept_time_minute = total_accept_time_minute + mentoring_report.accept_time
            total_count = total_count + 1

        project_dict = {
            'project': project,
            'mentoring_reports': mentoring_reports,
            'project_real_time_minute' : project_real_time_minute,
            'project_accept_time_minute' : project_accept_time_minute,
            'project_real_time' : get_strftime(project_real_time_minute),
            'project_accept_time' : get_strftime(project_accept_time_minute),
        }
        project_info_list.append(project_dict)

    mentor_info = {
        'mentor': mentor,
        'project_info_list': project_info_list,
        'total_real_time_minute': total_real_time_minute,
        'total_accept_time_minute': total_accept_time_minute,
        'total_real_time' : get_strftime(total_real_time_minute),
        'total_accept_time' : get_strftime(total_accept_time_minute),
        'total_count': total_count,
    }

    cur_time = datetime.today().replace(year=int(year), month=int(month))
    prev_month_time = cur_time + relativedelta(months = -1)
    next_month_time = cur_time + relativedelta(months = +1)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentor_info': mentor_info,
        'year': year,
        'month': month,

        'prev_year': prev_month_time.year,
        'prev_month': prev_month_time.month,
        'next_year': next_month_time.year,
        'next_month': next_month_time.month,
    }

    return render_to_response('manager/document_mentoring_report_mentee_monthly_detail.html', d, RequestContext(request))

def mentoring_report_project(request, type2):
    return HttpResponse('no')