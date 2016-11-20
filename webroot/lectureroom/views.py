#-*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .models import Lecture, LectureRoom, LectureBlock
from .forms import LectureForm

from django.contrib.auth.decorators import login_required as login

from time import mktime
from datetime import datetime
import re
import json

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# 강의실 예약 페이지 메인
@login
def main(request):

    return render_to_response('lectureroom/main.html', {})

# 최근 저장내용 가져오기
@login
def recent(request):
    data = {
        'success': False,
        'result': {}
    }

    lecture = Lecture.objects.filter(user=request.user).order_by('-created_at')[0]
    if not lecture:
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data['success'] = True
        data['result'] = {
            'name': lecture.name,
            'team': lecture.team,
            'count': lecture.count,
            'type': lecture.type,
            'admin': lecture.admin,
            'admin_tel': lecture.admin_tel,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')

# 강의실 예약 페이지
# 팝업으로 띄우기
@login
def new(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        start = request.POST.get('start_date', '')
        end = request.POST.get('end_date', '')

        try:
            # datetime 객체로 변환
            start = datetime.strptime(start, '%Y-%m-%d %p%I:%M')
            end = datetime.strptime(end, '%Y-%m-%d %p%I:%M')
        except Exception, e:
            print start, end
            return HttpResponse('<script> alert("올바른 시간형식이 아닙니다."); history.go(-1) </script>')

        if form.is_valid():
            # print type(form.cleaned_data['message'])
            # return HttpResponse('')
            user_object = request.user
            room_object = LectureRoom.objects.get(id=int(form.cleaned_data['room']))
            # print room_object
            result = Lecture.objects.new_lecture(
                user_object,
                form.cleaned_data['team'],
                form.cleaned_data['name'],
                room_object,
                int(form.cleaned_data['count']),
                form.cleaned_data['type'],
                start,
                end,
                form.cleaned_data['admin'],
                form.cleaned_data['admin_tel'].replace('-', ''),
                form.cleaned_data['message']
            )

            if result['success'] == True:
                return HttpResponse('<script> alert("강의실 예약이 완료되었습니다."); parent.location.reload(); window.close(); </script>')
        else:
            msg = ''
            for error in form.errors:
                if error == 'room':
                    msg = '강의실을 선택하세요.'
                elif error == 'name':
                    msg = '회의명을 입력해주세요.'
                elif error == 'team':
                    msg = '소속을 입력해주세요.'
                elif error == 'count':
                    msg = '참석 인원을 숫자로 입력해주세요.'
                elif error == 'admin':
                    msg = '담당자 이름을 입력해주세요.'
                elif error == 'admin_tel':
                    msg = '담당자 연락처를 입력해주세요.'
            return HttpResponse('<script> alert("' + msg + '"); history.go(-1) </script>')

    d = {}
    d['form'] = LectureForm()

    return render_to_response('lectureroom/new.html', d, RequestContext(request))

# 사용 가능한 강의실인지 확인
@login
def check(request):
    data = {
        'success': False,
        'available': False,
        'why': '',
    }

    room = request.POST.get('room', '')
    start = request.POST.get('start', '')
    end = request.POST.get('end', '')

    if not room:
        data['success'] = False
        data['why'] = '존재하지 않는 강의실입니다.'
        return HttpResponse(json.dumps(data), content_type='application/json')

    try:
        start = datetime.strptime(start, '%Y-%m-%d %p%I:%M')
        end = datetime.strptime(end, '%Y-%m-%d %p%I:%M')
    except Exception, e:
        data['success'] = False
        data['why'] = '올바른 시간 형식이 아닙니다.'
        return HttpResponse(json.dumps(data), content_type='application/json')

    if start == end:
        data['success'] = False
        data['why'] = '시작 날짜와 끝 날짜는 같을 수 없습니다.'
        return HttpResponse(json.dumps(data), content_type='application/json')

    room_object = LectureRoom.objects.get(id=int(room))

    if not room_object:
        data['success'] = False
        data['why'] = '존재하지 않는 강의실입니다.'
        return HttpResponse(json.dumps(data), content_type='application/json')

    available = Lecture.objects.check_lecture(room_object, start, end)
    if available == True:
        data['success'] = True
        data['available'] = True
    else:
        data['success'] = True
        data['available'] = False
        if type(available[0]) == LectureBlock:
            data['why'] = u'사용이 금지된 강의실입니다.\n' + available[0].name + '\n-----\n' + available[0].content + '\n-----\n' + str(available[0].start_date) + ' ~ ' + str(available[0].end_date)
        elif type(available[0]) == Lecture:
            data['why'] = u'이미 예약된 강의가 있습니다.'
        else:
            data['available'] = True

    return HttpResponse(json.dumps(data), content_type='application/json')

@login
def mylist(request):
    d = {}
    d['lectures'] = Lecture.objects.filter(start__gte=datetime.now(), user=request.user).order_by('start')

    return render_to_response('lectureroom/mylist.html', d, RequestContext(request))

@login
def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        if id == '':
            return

        lecture = Lecture.objects.get(id=id)
        if not lecture:
            return HttpResponse('<script> alert("존재하지 않는 예약입니다."); history.go(-1) </script>', status=500)

        # 본인만 삭제 가능
        if lecture.user != request.user and not request.user.is_staff:
            raise Http404

        lecture.delete()
        return HttpResponse('<script> alert("예약을 취소하였습니다."); window.close() </script>')

# 강의 예약목록 가져오기
@login
def list(request):
    data = {
        'success': 0,
        'result': [],
    }

    fr = request.GET.get('from', '')
    to = request.GET.get('to', '')

    if fr == '' or to == '':
        return HttpResponse(json.dumps(data), content_type='application/json')

    items = Lecture.objects.get_lecture(datetime.fromtimestamp(int(fr) / 1000), datetime.fromtimestamp(int(to) / 1000))
    data['success'] = 1
    if items['count'] == 0:
        return HttpResponse(json.dumps(data), content_type='application/json')

    for item in items['data']:
        data['result'].append({
            'id': item.id,
            'title': item.name,
            'url': '/lecture/view/' + str(item.id),
            'class': '',
            'room_id': item.room.id,
            'room_name': item.room.name,
            'admin': item.admin,
            'start': int(mktime(item.start.timetuple()) * 1000),
            'end': int(mktime(item.end.timetuple()) * 1000),
        })

    return HttpResponse(json.dumps(data), content_type='application/json')

@login
def view(request, id):
    if not Lecture.objects.filter(id=id).exists():
        raise Http404

    lecture = Lecture.objects.get(id=id)
    d = {
        'title': lecture.name,
        'lecture': lecture,
        'user': request.user,
    }

    return render_to_response('lectureroom/view.html', d, RequestContext(request))
