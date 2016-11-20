#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.html import escape
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# decorator
from django.contrib.auth.decorators import login_required

# python library
from time import mktime
import calendar
from calendar import monthrange
from datetime import datetime
from datetime import time as dt_time
from datetime import date as dt_date
import time
import re
import json

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

# Mail 모델
from mail.models import Mail

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


def index(request):
    return redirect('/admin/userlist')


@staff_login_required
def userlist(request):
    users = []
    modify_list = []
    type = request.GET.get('type', '')

    # 멘토/멘티 구분
    if type == 'mentee':
        users = User.objects.filter(type='1').filter(is_approval=True)
        title = '멘티 목록'
        subtitle = ''
        active_li = 'mentee'
    elif type == 'mentor':
        users = User.objects.filter(type='2').filter(is_approval=True)
        title = '멘토 목록'
        subtitle = ''
        active_li = 'mentor'
    elif type == 'staff':
        users = User.objects.filter(type='3').filter(is_approval=True)
        title = '관리자 목록'
        subtitle = ''

    # 멘티 기수 구분
    elif type == 'mentee1':
        users = User.objects.filter(type='1').filter(course_term='1').filter(is_approval=True)
        title = '멘티 (1기) 목록'
        subtitle = ''
        active_li = 'mentee1'

    elif type == 'mentee2':
        users = User.objects.filter(type='1').filter(course_term='2').filter(is_approval=True)
        title = '멘티 (2기) 목록'
        subtitle = ''
        active_li = 'mentee2'

    elif type == 'mentee3':
        users = User.objects.filter(type='1').filter(course_term='3').filter(is_approval=True)
        title = '멘티 (3기) 목록'
        subtitle = ''
        active_li = 'mentee3'

    elif type == 'mentee4':
        users = User.objects.filter(type='1').filter(course_term='4').filter(is_approval=True)
        title = '멘티 (4기) 목록'
        subtitle = ''
        active_li = 'mentee4'


    # 활성/비활성 구분
    elif type == 'approval':
        users = User.objects.filter(is_approval=True)
        title = '활성 사용자 목록'
        subtitle = '사무국에 사용 승인을 받은 사용자 목록입니다'
        active_li = 'approval'
    elif type == 'wait':
        users = User.objects.filter(is_approval=False)
        title = '승인 대기자 목록'
        subtitle = '사무국에 사용 승인을 받기 위해 대기중인 사용자 목록입니다'
        active_li = 'wait'
    else:
        users = User.objects.all()
        title = '전체 사용자 목록'
        subtitle = '승인 사용자, 승인 대기자, 관리자를 포함한 모든 사용자 목록입니다'
        active_li = 'all'

    d = {
        'modify_list': modify_list,
        'title': title,
        'subtitle': subtitle,
        'users': users,
        'active_li': active_li,
        'type': type,
    }

    return render_to_response('manager/userlist.html', d, RequestContext(request))

'''
userlist에서 select의 value값에 따라 submit된 값을 이용,
선택된 유저들을 편집한다

permission: 권한 변경
step: 단계 변경

'''
def modify_userlist(request):
    if request.method == 'POST':
        query_dict = request.POST
        user_list = query_dict.getlist('check_user_id')
        permission = query_dict['permission']
        step = query_dict['step']

        print 'check_user_id:', user_list
        print 'permission', permission

        # 권한 변경
        if permission != '':
            modify_permission(permission, user_list)

            user_text = u'유저 ('
            user_names_text = ''
            for i in range(len(user_list)):
                user = User.objects.get(id=user_list[i])
                name = user.first_name + user.last_name
                if i != len(user_list)-1:
                    user_names_text = user_names_text + name + ', '
                else:
                    user_names_text = user_names_text + name

            user_text = user_text + user_names_text + u')'
            log_text = user_text + u'의 권한 변경(' + permission + ')'

            log_type, exist = Log_Type.objects.get_or_create(title=u'유저 권한 변경')
            log = create_log(user=request.user,
                            type=log_type,
                            text=log_text)
            log.save()

        # 단계 변경
        if step != '':
            modify_step(step, user_list)

            user_text = u'유저 ('
            user_names_text = ''
            for i in range(len(user_list)):
                user = User.objects.get(id=user_list[i])
                name = user.first_name + user.last_name
                if i != len(user_list)-1:
                    user_names_text = user_names_text + name + ', '
                else:
                    user_names_text = user_names_text + name

            user_text = user_text + user_names_text + u')'
            log_text = user_text + u'의 단계 변경(' + step + ')'

            log_type, exist = Log_Type.objects.get_or_create(title=u'유저 단계 변경')
            log = create_log(user=request.user,
                            type=log_type,
                            text=log_text)
            log.save()

        return redirect('manager:userlist')
    else:
        return redirect('manager:userlist')

def convert(request):
    if request.method == 'POST':
        query_dict = request.POST
        user_id_list = query_dict.getlist('user_id')

        users = []
        for user_id in user_id_list:
            user = SomaUser.objects.get(id=user_id)
            if not user.type.title == u'관리자' or user.type.title == u'시스템 관리자':
                users.append(user)

        file_src = convert_excel(users)
        d = {
            'file_src': file_src,
        }

        data = open(file_src).read()
        resp = HttpResponse(data, content_type='application/x-download')
        resp['Content-Disposition'] = 'attachment;filename=convert.xls'
        return resp
    # return render_to_response("manager/convert_result.html", d)

def convert_excel(users):
    print 'convert_excel, users:', users
    start_row = 3
    start_column = 1

    book = Workbook()
    sheet1 = book.add_sheet('Users')

    info_title_list = [
        u'타입',
        u'상태',
        u'단계',
        u'아이디',
        u'이름',
        u'이메일',
        u'나이',
        u'성별',
        u'생일',
        u'주민등록번호',
        u'집 전화번호',
        u'휴대전화 번호',
        u'학력',
        u'병역',
        u'학교',
        u'주소',
        u'우편번호',
        u'구글 계정',
        u'트위터 계정',
        u'페이스북 계정',
    ]

    for i in range(len(info_title_list)):
        info_title = info_title_list[i]
        sheet1.write(start_row, start_column+i, info_title)

    for i in range(len(users)):
        user = users[i]
        print user

        type = user.type.title
        if user.type.title == u'멘티':
            type = type + "(" + user.course_term.title + user.course_step.title + ")"
        #elif user.type.title == u'관리자':
        #    continue
        #elif user.type.title == u'시스템 관리자':
        #    continue
        status = user.course_status.title
        step = user.course_step.title
        user_id = user.username
        name = user.last_name + user.first_name
        email = user.email
        age = user.age
        gender = user.get_gender_display()
        birthday = user.birthday.strftime("%Y-%m-%d")
        rr_number = user.rr_number
        home_number = user.home_number
        phone_number = user.phone_number
        education_level = user.education_level.title
        military = user.military.title
        school = user.school
        address = user.address1 + user.address2
        zipcode = user.zipcode
        google = user.google
        twitter = user.twitter
        facebook = user.facebook

        user_info_list = [
            type,
            status,
            step,
            user_id,
            name,
            email,
            age,
            gender,
            birthday,
            rr_number,
            home_number,
            phone_number,
            education_level,
            military,
            school,
            address,
            zipcode,
            google,
            twitter,
            facebook
        ]

        for j in range(len(user_info_list)):
            info = user_info_list[j]
            sheet1.write(start_row+1+i, start_column+j, info)

    #now = datetime.now().strftime("%Y-%m-%d.%H:%M:%S"),

    filename = "convert/" + 'user' + "abc" + ".xls"
    book.save(MEDIA_ROOT + "/" + filename)
    book.save(TemporaryFile())

    return MEDIA_ROOT + "/" + filename


def convert_mentoringreport(request):
    print 'convert_mentoringreport'
    if request.method == 'POST':
        query_dict = request.POST
        print query_dict
        document_id_list = query_dict.getlist('document_id')
        print document_id_list

        docs = []
        for doc_id in document_id_list:
            doc = MentoringReport.objects.get(id=doc_id)
            docs.append(doc)

        file_src = mentoringreport_excel(docs)
        d = {
            'file_src': file_src,
        }

        data = open(file_src).read()
        resp = HttpResponse(data, content_type='application/x-download')
        resp['Content-Disposition'] = 'attachment;filename=mentoringreport.xls'
        return resp
    # return render_to_response("manager/convert_result.html", d)

def mentoringreport_excel(mentoringreport_list):
    from mobile.api import convert_strftime_minute, convert_strftime_time, convert_strftime_day
    print 'mentoringreport_excel, reports:', mentoringreport_list
    start_row = 0
    start_column = 0

    book = Workbook()
    sheet1 = book.add_sheet('MentoringReports')

    info_title_list = [
        u'타입',
        u'프로젝트',
        u'멘토',
        u'협업벤토링 여부',
        u'멘티',
        u'멘토링 날짜',
        u'멘토링 장소',
        u'시작 시간',
        u'종료 시간',
        u'실제 시간',
        u'인정 시간',
        u'보고서 제목',

        u'멘토 의견',
        u'계획사항',
        u'특이사항',
        u'보고서 내용',
    ]

    for i in range(len(info_title_list)):
        info_title = info_title_list[i]
        sheet1.write(start_row, start_column+i, info_title)

    for i in range(len(mentoringreport_list)):
        report = mentoringreport_list[i]
        print report

        type = report.type.title
        project = report.project.title
        mentor = report.mentor.last_name + report.mentor.first_name
        is_cooperation = report.is_cooperation

        str_mentees = ''
        for k in range(len(report.mentees.all())):
            mentee = report.mentees.all()[k]
            str_mentees += (mentee.last_name + mentee.first_name)
            if not k == len(report.mentees.all())-1:
                str_mentees += u', '

        mentees = str_mentees
        date = convert_strftime_day(report.date)
        place = report.place
        start_time = convert_strftime_minute(report.start_time)
        end_time = convert_strftime_minute(report.end_time)
        real_time = convert_strftime_minute(report.real_time)
        accept_time = convert_strftime_minute(report.accept_time)
        title = report.title
        content = report.content
        opinion = report.opinion
        schedule = report.schedule
        issue = report.issue

        info_list = [
            type,
            project,
            mentor,
            is_cooperation,
            mentees,
            date,
            place,
            start_time,
            end_time,
            real_time,
            accept_time,
            title,

            opinion,
            schedule,
            issue,
            content,
        ]

        for j in range(len(info_list)):
            print 'row:', (1+i), ' col:', j
            info = info_list[j]
            sheet1.write(start_row+1+i, start_column+j, info)

    #now = datetime.now().strftime("%Y-%m-%d.%H:%M:%S"),

    filename = "convert/" + 'mentoringreport' + ".xls"
    book.save(MEDIA_ROOT + "/" + filename)
    book.save(TemporaryFile())

    return MEDIA_ROOT + "/" + filename

@staff_login_required
def user_profile(request, id):
    user = SomaUser.objects.get(id=id)

    awards = Award.objects.filter(member=user).order_by('-date')
    careers = Career.objects.filter(member=user).order_by('-end_date')
    d = {
        'user': user,
        'awards': awards,
        'careers': careers,
    }

    return render_to_response('member/profile.html', d)

@staff_login_required
def mail_staff(request):
    title = u'관리자 메일 설정'
    subtitle = u'각 관리자 계정의 메일 수신 여부를 설정합니다'
    active_li = 'staff'

    receive_staffs = User.objects.filter(is_staff=True).filter(is_receive_staff_mail=True)
    not_receive_staffs = User.objects.filter(is_staff=True).filter(is_receive_staff_mail=False)
    staffs = User.objects.filter(is_staff=True)

    d = {
        'title': title,
        'subtitle': subtitle,
        'active_li': active_li,
        'staffs': staffs,
        'receive_staffs': receive_staffs,
        'not_receive_staffs': not_receive_staffs,
    }
    return render_to_response('manager/mail_staff.html', d, RequestContext(request))

@staff_login_required
def edit_mail_staff(request):
    if request.method == 'POST':
        query_dict = request.POST
        checked_staff_id_list = query_dict.getlist('check_staff_id')
        staff_list = User.objects.filter(is_staff=True)

        for staff in staff_list:
            staff.is_receive_staff_mail = False
            staff.save()

        for checked_staff_id in checked_staff_id_list:
            staff = User.objects.get(id=checked_staff_id)
            staff.is_receive_staff_mail = True
            staff.save()

        # 리다이렉트 하는 mail_staff뷰에 success메세지 보냄(템플릿에서 판단해서 modal띄워줌)
        messages.add_message(request, messages.SUCCESS, 'Hello')
        return redirect('manager:mail_staff')
    else:
        return redirect('manager:mail_staff')

@csrf_exempt
@staff_login_required
def mail_check(request):
    if request.method == 'POST':
        start = int(request.POST.get('iDisplayStart', ''))
        len = int(request.POST.get('iDisplayLength', ''))

        mails = Mail.objects.all()[start:len]
        data = {
            'sEcho': 1,
            'iTotalRecords': Mail.objects.count(),
            'iTotalDisplayRecords': mails.__len__(),
            'aaData': [],
        }

        for mail in mails:
            send_stat = ''
            if mail.status == '1':
                send_stat = '발송 대기'
            elif mail.status == '2':
                send_stat = '발송중'
            elif mail.status == '3':
                send_stat = mail.send_at.strftime("%Y/%m/%d %H:%M")
            elif mail.status == '4':
                send_stat = '발송 실패'
            data['aaData'].append([
                mail.id, mail.mail_from.username, mail.mail_to.username, mail.mail.title, send_stat, ( '읽지 않음', mail.read_at.strftime("%Y/%m/%d %H:%M") )[ mail.read ]
            ])

        return HttpResponse(json.dumps(data), content_type='application/json')

    d = {
        'title': '메일 발송상태 확인',
        'subtitle': '메일 발송상태 및 수신상태를 확인합니다',
    }

    return render_to_response('manager/mail_check.html', d)

@staff_login_required
def lecturelist(request):
    title = ''
    subtitle = ''

    lectures = Lecture.objects.all()

    d = {
        'title': title,
        'subtitle': subtitle,
        'lectures': lectures,
    }
    return render_to_response('manager/lecturelist.html', d)

@csrf_exempt
@staff_login_required
def view_lecturelist(request):
    room = request.GET.get('room', '')
    if not LectureRoom.objects.filter(id=room).exists():
        raise Http404
    room = LectureRoom.objects.get(id=room)

    if request.method == 'POST':
        start = int(request.POST.get('iDisplayStart', ''))
        len = int(request.POST.get('iDisplayLength', ''))

        lectures = Lecture.objects.filter(room=room)[start:len]
        data = {
            'sEcho': 1,
            'iTotalRecords': Lecture.objects.filter(room=room).__len__(),
            'iTotalDisplayRecords': lectures.__len__(),
            'aaData': [],
        }

        for lecture in lectures:
            data['aaData'].append([
                lecture.id, "%s ~ %s" % ( lecture.start.strftime("%Y/%m/%d %H시"), lecture.end.strftime("%Y/%m/%d %H시") ), lecture.name, lecture.count, lecture.admin
            ])

        return HttpResponse(json.dumps(data), content_type='application/json')

    d = {
        'title': room.name,
        'subtitle': '선택한 강의실의 예약목록을 확인합니다.',
    }

    return render_to_response('manager/view_lecturelist.html', d)

@csrf_exempt
@staff_login_required
def lectureroom(request):
    d = {}
    if request.method == 'POST':
        type = request.POST.get('type', '')

        if type == 'new':
            name = request.POST.get('room_name', '')
            if name == '':
                d['alert'] = '강의실 이름을 입력하세요.'
                d['alert_type'] = 'danger'
            elif LectureRoom.objects.filter(name=name).exists():
                d['alert'] = '이미 존재하는 강의실입니다.'
                d['alert_type'] = 'danger'
            else:
                LectureRoom.objects.create(name=name)
                d['alert'] = '강의실이 등록되었습니다.'
                d['alert_type'] = 'success'
        elif type == 'edit':
            id = request.POST.get('id', '')
            new_name = request.POST.get('new_name', '')
            if not LectureRoom.objects.filter(id=id).exists():
                return HttpResponse(json.dumps({ 'result': False }), mimetype='application/json')

            room = LectureRoom.objects.get(id=id)
            room.name = new_name
            room.save()

            return HttpResponse(json.dumps({ 'result': True }), mimetype='application/json')

    rooms = LectureRoom.objects.all()

    d['title'] = '강의실 관리'
    d['subtitle'] = '강의실 목록을 관리합니다.'
    d['rooms'] = rooms

    return render_to_response('manager/lectureroom.html', d, RequestContext(request))

@staff_login_required
def lectureroom_remove(request):
    d = {}
    if request.method == 'POST':
        room_id = request.POST.get('room_id', '')

        if room_id == '':
            d['message'] = '올바른 강의실을 선택하세요.'
        elif LectureRoom.objects.filter(id=room_id).count() == 0:
            d['message'] = '존재하지 않는 강의실입니다.'
        else:
            LectureRoom.objects.filter(id=room_id).delete()
            d['message'] = '강의실이 삭제되었습니다.'

    return HttpResponse("<script> alert('" + d['message'] + "'); location.replace('../room'); </script>")

@staff_login_required
def lectureblock(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        data = request.POST.get('data', '')
        if action == 'remove' and data != '':
            arr = json.loads(data)
            for item in arr:
                block = LectureBlock.objects.get(id=int(item))
                if block:
                    block.delete()
            return HttpResponse('<script> alert("선택 항목이 삭제되었습니다."); location.replace("./block") </script>')

    d = {}
    d['title'] = '강의실 차단(사용불가) 관리'
    d['subtitle'] = '강의실 예약을 할 수 없도록 설정합니다.'

    d['blocks'] = LectureBlock.objects.all()
    return render_to_response('manager/lectureblock.html', d, RequestContext(request))

@staff_login_required
def lectureblock_new(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        content = request.POST.get('content', '')
        start = request.POST.get('start_date', '').replace(u'오전', 'AM').replace(u'오후', 'PM')
        end = request.POST.get('end_date', '').replace(u'오전', 'AM').replace(u'오후', 'PM')

        if name == '' or content == '':
            return HttpResponse('<script> alert("차단 명칭 및 사유를 입력해주세요."); history.go(-1) </script>')

        try:
            start = datetime.strptime(start, '%Y-%m-%d %p%I:%M')
            end = datetime.strptime(end, '%Y-%m-%d %p%I:%M')
        except Exception, e:
            return HttpResponse('<script> alert("올바른 날짜/시간 형식이 아닙니다."); history.go(-1) </script>')

        for rid in request.POST.getlist('rooms[]'):
            room = LectureRoom.objects.get(id=rid)
            LectureBlock.objects.new_block(name, content, start, end, room)


        return HttpResponse('<script> alert("새 차단 규칙이 추가되었습니다."); location.replace("./") </script>')

    d = {}
    d['rooms'] = LectureRoom.objects.all()

    return render_to_response('manager/lectureblock_new.html', d, RequestContext(request))

@staff_login_required
def lecture_dashboard(request):
    def add_month(sourcedate, months):
         month = sourcedate.month - 1 + months
         year = sourcedate.year + month / 12
         month = month % 12 + 1
         day = min(sourcedate.day, calendar.monthrange(year, month)[1])
         return dt_date(year, month, day)

    today_min = datetime.combine(datetime.today(), dt_time.min)
    today_max = datetime.combine(datetime.today(), dt_time.max)
    d = {
        'title': '대쉬보드',
        'subtitle': '',
        'stat': {
            'today': Lecture.objects.filter(start__range=(today_min, today_max)).count(),
        },
    }

    month = datetime(int(request.GET.get('y', datetime.today().year)), int(request.GET.get('m', datetime.today().month)), 1)
    last_month = datetime(month.year, month.month, monthrange(month.year, month.month)[1])

    d['min_date'] = min_date = datetime.combine(month, dt_time.min)
    d['max_date'] = max_date = datetime.combine(last_month, dt_time.max)
    d['prev_date'] = prev_date = add_month(month, -1)
    d['next_date'] = next_date = add_month(month, 1)
    d['lectures'] = lectures = list(reversed(Lecture.objects.filter(start__range=(min_date, max_date))))
    d['rooms_count'] = {}
    for lecture in lectures:
        if not lecture.room.name in d['rooms_count']:
            d['rooms_count'][lecture.room.name] = 0
        d['rooms_count'][lecture.room.name] += 1

    return render_to_response('manager/lecture_dashboard.html', d)

def only_admin(request):
    return render_to_response('manager/need_staff_permission.html')
