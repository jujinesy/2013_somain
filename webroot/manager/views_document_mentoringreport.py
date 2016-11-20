#-*- coding: utf-8 -*-
import pdb
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# python library
from nptime import nptime
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Proejct 모델
from project.models import *

# Document 모델
from document.models import *
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter 
def multiply(value, arg): 
    return int(value) * int(arg) 

class TotalInfo:
    real_time = nptime(0, 0)
    accept_time = nptime(0, 0)
    count = 0

class ProjectInfo:
    real_time = nptime(0, 0)
    accept_time = nptime(0, 0)

# 시간연산시 사용
def get_timedelta(time):
    return timedelta(hours=time.hour, minutes=time.minute)

def last_day_of_month(cur_date):
    date1 = cur_date + relativedelta(months = +1)
    # print 'date1', date1
    date2 = date1.replace(day=1)
    # print 'date2', date2
    date3 = date2 - timedelta(days=1)
    # print 'date3', date3
    return date3.day

def get_project_info(mentoringreport_filter_dict, project):
    mentoringreports = MentoringReport.objects.filter(**mentoringreport_filter_dict)
    
    projectinfo = ProjectInfo()

    for mentoringreport in mentoringreports:
        projectinfo.real_time = projectinfo.real_time + get_timedelta(mentoringreport.real_time)
        projectinfo.accept_time = projectinfo.accept_time + get_timedelta(mentoringreport.accept_time)

    project_dict = {
        'project': project,
        'mentoringreports': mentoringreports,
        'project_real_time' : projectinfo.real_time.strftime("%H:%M"),
        'project_accept_time' : projectinfo.accept_time.strftime("%H:%M"),
        'project_real_time_data': projectinfo.real_time,
        'project_accept_time_data': projectinfo.accept_time,
    }
    return project_dict

def get_mentor_info(mentor, mentoringreport_filter_dict):
    projects = Project.objects.filter(mentor=mentor)
    project_info_list = []

    totalinfo = TotalInfo()

    for project in projects:
        mentoringreport_filter_dict['project'] = project
        project_dict = get_project_info(mentoringreport_filter_dict, project)

        totalinfo.real_time = totalinfo.real_time + get_timedelta(project_dict['project_real_time_data'])
        totalinfo.accept_time = totalinfo.accept_time + get_timedelta(project_dict['project_accept_time_data'])
        totalinfo.count = totalinfo.count + project_dict['mentoringreports'].count()
        project_info_list.append(project_dict)

    mentor_dict = {
        'mentor': mentor,
        'project_info_list': project_info_list,
        'totalinfo': totalinfo,
        'total_real_time': totalinfo.real_time.strftime("%H:%M"),
        'total_accept_time': totalinfo.accept_time.strftime("%H:%M"),
        'total_count': totalinfo.count,
    }
    return mentor_dict

def get_mentee_info(mentee, mentoringreport_filter_dict):
    projects = Project.objects.filter(mentees=mentee)
    project_info_list = []
    totalinfo = TotalInfo()

    for project in projects:
        mentoringreport_filter_dict['project'] = project
        project_dict = get_project_info(mentoringreport_filter_dict, project)

        totalinfo.real_time = totalinfo.real_time + get_timedelta(project_dict['project_real_time_data'])
        totalinfo.accept_time = totalinfo.accept_time + get_timedelta(project_dict['project_accept_time_data'])
        project_info_list.append(project_dict)

    mentee_dict = {
        'mentee': mentee,
        'project_info_list': project_info_list,
        'totalinfo': totalinfo,
        'total_real_time': totalinfo.real_time.strftime("%H:%M"),
        'total_accept_time': totalinfo.accept_time.strftime("%H:%M"),
        'total_count': totalinfo.count,
    }

    return mentee_dict

'''
'type2'의 값에 따라 min_date와 max_date dictionary를 반환한다
monthly
    주어진 값이 있을경우 그대로 반환
    연, 월이 주어질 경우 해당 연 월을 기준으로 1일과 마지막날을 반환
    주어진 값이 없을 경우 오늘을 기준으로 1일과 마지막날을 반환
monthly2
    주어진 값이 있을경우 그대로 반환
    연, 월이 주어질 경우 해당 연 월을 기준으로 지난달 21일부터 해당 연월 20일까지를 반환
    주어진 값이 없을 경우 오늘을 기준으로
        오늘이 21일 이상일 경우 이번달 21일부터 다음달 20일까지를 반환
        오늘이 20일 이하일 경우 지난달 21일부터 이번달 20일까지를 반환

연, 월로 계산하지않고 템플릿에서 date객체를 만들어서 인자로 넘겨줄 수 있도록 한다
'''

def get_date_info(query_dict):
    today = date.today()
    if query_dict['type2'] == 'monthly':
        if query_dict.has_key('min_date') and query_dict.has_key('max_date'):
            min_date = datetime.strptime(query_dict['min_date'], '%Y-%m-%d').date()
            max_date = datetime.strptime(query_dict['max_date'], '%Y-%m-%d').date()
        elif query_dict.has_key('year') and query_dict.has_key('month'):
            year = int(query_dict['year'])
            month = int(query_dict['month'])
            cur_day = datetime(year=year, month=month, day=1).date()
            min_date = cur_day.replace(day=1)
            max_date = cur_day.replace(day=last_day_of_month(min_date))
        else:
            min_date = today.replace(day=1)
            max_date = today.replace(day=last_day_of_month(today))
        prev_min_date = (min_date + relativedelta(months = -1)).replace(day=1)
        prev_max_date = (max_date + relativedelta(months = -1)).replace(day=last_day_of_month(prev_min_date))
        next_min_date = (min_date + relativedelta(months = +1)).replace(day=1)
        next_max_date = (max_date + relativedelta(months = +1)).replace(day=last_day_of_month(next_min_date))

    elif query_dict['type2'] == 'monthly2':
        if query_dict.has_key('max_date') and query_dict.has_key('max_date'):
            min_date = datetime.strptime(query_dict['min_date'], '%Y-%m-%d').date()
            max_date = datetime.strptime(query_dict['max_date'], '%Y-%m-%d').date()
        elif query_dict.has_key('year') and query_dict.has_key('month'):
            year = int(query_dict['year'])
            month = int(query_dict['month'])
            cur_day = datetime(year=year, month=month, day=1).date()
            min_date = (cur_day + relativedelta(months = -1)).replace(day=21)
            max_date = cur_day.replace(day=20)
        else:
            if today.day > 20:
                min_date = today.replace(day=21)
                max_date = (today + relativedelta(months = +1)).replace(day=20)
            else:
                min_date = (today + relativedelta(months = -1)).replace(day=21)
                max_date = today.replace(day=20)
        
        prev_min_date = (min_date + relativedelta(months = -1)).replace(day=21)
        prev_max_date = (max_date + relativedelta(months = -1)).replace(day=20)
        next_min_date = (min_date + relativedelta(months = +1)).replace(day=21)
        next_max_date = (max_date + relativedelta(months = +1)).replace(day=20)

    elif query_dict['type2'] == 'period':
        if query_dict.has_key('start_year') and query_dict.has_key('start_month') and query_dict.has_key('start_day') and query_dict.has_key('end_year') and query_dict.has_key('end_month') and query_dict.has_key('end_day'):

            min_date = datetime.strptime(query_dict['start_year']+'-'+query_dict['start_month']+'-'+query_dict['start_day'], '%Y-%m-%d').date()
            max_date = datetime.strptime(query_dict['end_year']+'-'+query_dict['end_month']+'-'+query_dict['end_day'], '%Y-%m-%d').date()
            prev_min_date = None
            prev_max_date = None
            next_min_date = None
            next_max_date = None
        else:
            pass

    date_info = {
        'min_date': min_date, 
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,
    }
    return date_info

'''
각 분류별 조건에 맞는 결과 목록을 보여준다.
상세화면은 detail로
monthly, monthly2, period의 분류는 마지막 render_to_response에서 템플릿만 변경해서 활용
'''
def mentoringreport_mentor_list(request):
    query_dict = request.POST
    today = date.today()
    type1 = query_dict['type1']
    type2 = query_dict['type2']
    print 'mentoringreport_mentor_list, type2:', type2

    if query_dict.has_key('mentor'):
        return mentoringreport_mentor_detail(request)

    date_info = get_date_info(query_dict)
    min_date = date_info['min_date']
    max_date = date_info['max_date']
    prev_min_date = date_info['prev_min_date']
    prev_max_date = date_info['prev_max_date']
    next_min_date = date_info['next_min_date']
    next_max_date = date_info['next_max_date']

    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentors = User.objects.filter(type__title=u'멘토')

    mentor_info_list = []
    for mentor in mentors:
        mentoringreport_filter_dict = {
            'is_submitted': True,
            'date__gte': min_date,
            'date__lte': max_date,
        }
        mentor_dict = get_mentor_info(mentor, mentoringreport_filter_dict)
        mentor_info_list.append(mentor_dict)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentor_info_list': mentor_info_list,
        
        'type1': type1,
        'type2': type2,
        'min_date': min_date,
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,
    }

    if type2 == 'monthly' or type2 == 'monthly2':
        return render_to_response('manager/document/mentoringreport/mentor_list_monthly.html', d, RequestContext(request))
    elif type2 == 'period':
        print 'mentor, period'
        return render_to_response('manager/document/mentoringreport/mentor_list_period.html', d, RequestContext(request))

def mentoringreport_mentee_list(request):
    query_dict = request.POST
    now = datetime.now()

    if query_dict.has_key('mentee'):
        return mentoringreport_mentee_detail(request)

    type1 = query_dict['type1']
    type2 = query_dict['type2']
    print 'mentoringreport_mentee_list, type2:', type2

    date_info = get_date_info(query_dict)
    min_date = date_info['min_date']
    max_date = date_info['max_date']
    prev_min_date = date_info['prev_min_date']
    prev_max_date = date_info['prev_max_date']
    next_min_date = date_info['next_min_date']
    next_max_date = date_info['next_max_date']

    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    mentees = User.objects.filter(type__title=u'멘티')

    mentee_info_list = []
    for mentee in mentees:
        mentoringreport_filter_dict = {
            'is_submitted': True,
            'date__gte': min_date,
            'date__lte': max_date,
            'mentees': mentee,
        }
        mentee_dict = get_mentee_info(mentee, mentoringreport_filter_dict)
        mentee_info_list.append(mentee_dict)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentee_info_list': mentee_info_list,

        'type1': type1,
        'type2': type2,
        'min_date': min_date,
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,
    }
    if type2 == 'monthly' or type2 == 'monthly2':
        return render_to_response('manager/document/mentoringreport/mentee_list_monthly.html', d, RequestContext(request))
    elif type2 == 'period':
        return render_to_response('manager/document/mentoringreport/mentee_list_period.html', d, RequestContext(request))

def mentoringreport_project_list(request):
    query_dict = request.POST
    now = datetime.now()

    if query_dict.has_key('project_id'):
        return mentoringreport_project_detail(request)

    date_info = get_date_info(query_dict)
    min_date = date_info['min_date']
    max_date = date_info['max_date']
    prev_min_date = date_info['prev_min_date']
    prev_max_date = date_info['prev_max_date']
    next_min_date = date_info['next_min_date']
    next_max_date = date_info['next_max_date']

    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    projects = Project.objects.filter(is_finished=False)
    project_info_list = []
    for project in projects:
        mentoringreport_filter_dict = {
            'is_submitted': True,
            'date__gte': min_date,
            'date__lte': max_date,
            'project': project,
        }        
        project_info = get_project_info(mentoringreport_filter_dict, project)
        project_info_list.append(project_info)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'project_info_list': project_info_list,
        
        'type1': query_dict['type1'],
        'type2': query_dict['type2'],
        'min_date': min_date,
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,
    }
    return render_to_response('manager/document/mentoringreport/project_list_monthly.html', d, RequestContext(request))

def mentoringreport_total_list(request):
    query_dict = request.POST
    if query_dict.has_key('type1'):
        type1 = query_dict['type1']
    else:
        type1 = 'total'

    if query_dict.has_key('type2'):
        type2 = query_dict['type2']
    else:
        type2 = 'monthly'
        query_dict = {
            'type1': type1,
            'type2': type2,
        }

    date_info = get_date_info(query_dict)
    min_date = date_info['min_date']
    max_date = date_info['max_date']
    prev_min_date = date_info['prev_min_date']
    prev_max_date = date_info['prev_max_date']
    next_min_date = date_info['next_min_date']
    next_max_date = date_info['next_max_date']
    # print date_info

    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    # Mentor 정보
    mentors = User.objects.filter(type__title=u'멘토')
    mentor_info_list = []
    for mentor in mentors:
        mentoringreport_filter_dict = {
            'is_submitted': True,
            'date__gte': min_date,
            'date__lte': max_date,
        }
        mentor_dict = get_mentor_info(mentor, mentoringreport_filter_dict)
        mentor_info_list.append(mentor_dict)
    
    # Mentee 정보
    mentees = User.objects.filter(type__title=u'멘티')
    mentee_info_list = []
    mentee_info_list_0 = []
    mentee_info_list_1 = []
    mentee_info_list_2 = []
    mentee_info_list_3 = []
    mentee_info_list_4 = []
    for mentee in mentees:
        try:
            project = Project.objects.filter(is_finished=False).get(mentees=mentee)
        except Project.DoesNotExist:
            project = None

        mentoringreport_filter_dict = {
            'is_submitted': True,
            'mentees': mentee,
            'date__gte': min_date,
            'date__lte': max_date,
        }
        project_info = get_project_info(mentoringreport_filter_dict, project)

        mentee_dict = {
            'mentee': mentee,
            'project_info': project_info,
        }
        # mentee_info_list.append(mentee_dict)
        # print mentee
        # print project_info['mentoringreports'].count()
        # print '-\n'
        if project_info['mentoringreports'].count() == 0:
            mentee_info_list_0.append(mentee_dict)
        elif project_info['mentoringreports'].count() == 1:
            mentee_info_list_1.append(mentee_dict)
        elif project_info['mentoringreports'].count() == 2:
            mentee_info_list_2.append(mentee_dict)
        elif project_info['mentoringreports'].count() == 3:
            mentee_info_list_3.append(mentee_dict)
        elif project_info['mentoringreports'].count() >= 4:
            mentee_info_list_4.append(mentee_dict)

    mentee_info_lists = [
        {
            'title': u'0번',
            'list': mentee_info_list_0,
        },
        {
            'title': u'1번',
            'list': mentee_info_list_1,
        },
        {
            'title': u'2번',
            'list': mentee_info_list_2,
        },
        {
            'title': u'3번',
            'list': mentee_info_list_3,
        },
        {
            'title': u'4번 이상',
            'list': mentee_info_list_4,
        },
    ]

    mentoring_report_full = MentoringReport.objects.filter(date__gte=min_date).filter(date__lte=max_date)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'type1': type1,
        'type2': type2,
        'min_date': min_date,
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,

        'mentor_info_list': mentor_info_list,
        'mentee_info_lists': mentee_info_lists,
        'mentee_info_list': mentee_info_list,
        'mentee_info_list_0': mentee_info_list_0,
        'mentee_info_list_1': mentee_info_list_1,
        'mentee_info_list_2': mentee_info_list_2,
        'mentee_info_list_3': mentee_info_list_3,
        'mentee_info_list_4': mentee_info_list_4,
        
        'mentoring_report_full': mentoring_report_full,
    }

    return render_to_response('manager/document/mentoringreport/total_list_monthly.html', d, RequestContext(request))




'''
월별 상세 통계 (각 멘토, 멘티 또는 프로젝트 별 )
'''
def mentoringreport_mentor_detail(request):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    query_dict = request.POST
    type1 = query_dict['type1']
    type2 = query_dict['type2']

    if not query_dict.has_key('mentor'):
        return HttpResponse('No mentor query')
    
    mentor = User.objects.get(username=query_dict['mentor'])
    date_info = get_date_info(query_dict)
    min_date = date_info['min_date']
    max_date = date_info['max_date']
    prev_min_date = date_info['prev_min_date']
    prev_max_date = date_info['prev_max_date']
    next_min_date = date_info['next_min_date']
    next_max_date = date_info['next_max_date']

    mentoringreport_filter_dict = {
        'is_submitted': True,
        'date__gte': min_date,
        'date__lte': max_date,
    }
    mentor_info = get_mentor_info(mentor, mentoringreport_filter_dict)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentor_info': mentor_info,

        'type1': type1,
        'type2': type2,
        'min_date': min_date,
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,
    }
    print 'mentoringreport_mentor_detail, type1:', type1, 'type2:', type2, 'mentor:', mentor
    if type2 == 'monthly' or type2 == 'monthly2':
        return render_to_response('manager/document/mentoringreport/mentor_detail_monthly.html', d, RequestContext(request))
    elif type2 == 'period':
        return render_to_response('manager/document/mentoringreport/mentor_detail_period.html', d, RequestContext(request))

def mentoringreport_mentee_detail(request):
    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    query_dict = request.POST
    type1 = query_dict['type1']
    type2 = query_dict['type2']

    if not query_dict.has_key('mentee'):
        return HttpResponse('No mentee query')
    
    mentee = User.objects.get(username=query_dict['mentee'])
    date_info = get_date_info(query_dict)
    min_date = date_info['min_date']
    max_date = date_info['max_date']
    prev_min_date = date_info['prev_min_date']
    prev_max_date = date_info['prev_max_date']
    next_min_date = date_info['next_min_date']
    next_max_date = date_info['next_max_date']

    mentoringreport_filter_dict = {
        'mentees': mentee,
        'is_submitted': True,
        'date__gte': min_date,
        'date__lte': max_date,
    }
    mentee_info = get_mentee_info(mentee, mentoringreport_filter_dict)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'mentee_info': mentee_info,
        
        'type1': type1,
        'type2': type2,
        'min_date': min_date,
        'max_date': max_date,
        'prev_min_date': prev_min_date,
        'prev_max_date': prev_max_date,
        'next_min_date': next_min_date,
        'next_max_date': next_max_date,
    }
    if type2 == 'monthly' or type2 == 'monthly2':
        return render_to_response('manager/document/mentoringreport/mentee_detail_monthly.html', d, RequestContext(request))
    elif type2 == 'period':
        return render_to_response('manager/document/mentoringreport/mentee_detail_period.html', d, RequestContext(request))

def mentoringreport_project_detail(request):
    query_dict = request.POST
    now = datetime.now()

    if query_dict.has_key('year'):
        year = query_dict['year']
    else:
        year = now.year

    if query_dict.has_key('month'):
        month = query_dict['month']
    else:
        month = now.month

    title = u'온라인 서류제출'
    subtitle = u'온라인 서류제출 현황을 보여줍니다'
    active_li = 'all'

    project = Project.objects.get(id=int(query_dict['project_id']))
    mentoringreport_filter_dict = {
        'is_submitted': True,
        'date__year': year,
        'date__month': month,
    }
    project_info = get_project_info(mentoringreport_filter_dict, project)

    cur_time = datetime.today().replace(year=int(year), month=int(month))
    prev_month_time = cur_time + relativedelta(months = -1)
    next_month_time = cur_time + relativedelta(months = +1)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,

        'type1': query_dict['type1'],
        'type2': query_dict['type2'],

        'project_info': project_info,
        'year': year,
        'month': month,

        'prev_year': prev_month_time.year,
        'prev_month': prev_month_time.month,
        'next_year': next_month_time.year,
        'next_month': next_month_time.month,
    }
    return render_to_response('manager/document/mentoringreport/mentoringreport_project_detail_monthly.html', d, RequestContext(request))


'''
기간별 통계
'''
# 기간 선택 후 결과 화면 이동
# def mentoringreport_period(request):
#     query_dict = request.POST
#     type1 = query_dict['type1']
#     type2 = query_dict['type2']

#     title = u'온라인 서류제출'
#     subtitle = u'온라인 서류제출 현황을 보여줍니다'
#     active_li = 'all'

#     date_info = get_date_info(query_dict)
#     min_date = date_info['min_date']
#     max_date = date_info['max_date']

#     d = {
#         'title': title,
#         'subtitle': subtitle,
#         'active_li': active_li,

#         'type1': type1,
#         'type2': type2,
#         'min_date': min_date,
#         'max_date': max_date,
#     }

#     if type1 == 'mentor':
#         if query_dict.has_key('mentor'):
#             ''' 특정 멘토 기간 검색일 경우 월별/단계별 시 사용할 mentor정보 전달, 템플릿에서 사용 '''
#             mentor = User.objects.get(username=query_dict['mentor'])
#             period_title = mentor.last_name + mentor.first_name + u' 멘토 기간 검색 결과'
#             mentor_dict = { 'mentor': mentor, }
#             d['mentor_info'] = mentor_dict
#         else:
#             period_title = u'멘토 기간 검색 결과'
#     elif type1 == 'mentee':
#         if query_dict.has_key('mentee'):
#             mentee = User.objects.get(username=query_dict['mentee'])
#             period_title = mentee.last_name + mentee.first_name + u' 멘티 기간 검색 결과'
#         else:
#             period_title = u'멘티 기간 검색 결과'
#     elif type1 == 'project':
#         if query_dict.has_key('project_id'):
#             project = Project.objects.get(id=int(query_dict['project_id']))
#             period_title = project.title + u' 프로젝트 기간 검색 결과'
#         else:
#             period_title = u'프로젝트 기간 검색 결과'
#     elif type1 == 'total':
#         period_title = u'전체 멘토링보고서 기간 검색 결과'

#     d['period_title'] = period_title

#     return render_to_response('manager/document/mentoringreport_period.html', d, RequestContext(request))