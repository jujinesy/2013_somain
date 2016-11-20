#-*- coding: utf-8 -*-
from django.db import models


# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# member
from member.models import *

'''
modify_userlist에서 사용
request.POST['permission']의 값에 따라 작동
유저 권한을 변경
'''
def modify_permission(permission, user_list):
    if permission == 'approval':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.is_approval = True
            cur_user.save()
    elif permission == 'wait':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.is_approval = False
            cur_user.save()
    elif permission == 'mentor':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.type = Type.objects.get(title=u'멘토')
            cur_user.save()
    elif permission == 'mentee1':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.type = Type.objects.get(title=u'멘티')
            cur_user.course_term = CourseTerm.objects.get(title=u'1기')
            cur_user.save()
    elif permission == 'mentee2':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.type = Type.objects.get(title=u'멘티')
            cur_user.course_term = CourseTerm.objects.get(title=u'2기')
            cur_user.save()
    elif permission == 'mentee3':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.type = Type.objects.get(title=u'멘티')
            cur_user.course_term = CourseTerm.objects.get(title=u'3기')
            cur_user.save()
    elif permission == 'mentee4':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.type = Type.objects.get(title=u'멘티')
            cur_user.course_term = CourseTerm.objects.get(title=u'4기')
            cur_user.save()
    elif permission == 'staff':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.type = Type.objects.get(title=u'관리자')
            cur_user.save()
    else:
        return 'None'
'''
modify_userlist에서 사용
request.POST['step']의 값에 따라 작동
유저 단계를 변경
'''
def modify_step(step, user_list):
    if step == '1st-1':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'1단계-1차')
            cur_user.save()
    elif step == '1st-2':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'1단계-2차')
            cur_user.save()
    elif step == '2nd':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'2단계')
            cur_user.save()
    elif step == '3rd':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'3단계')
            cur_user.save()
    elif step == 'certificate':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'인증자')
            cur_user.save()
    elif step == 'giveup(1st-1)':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'포기자(1단계-1차)')
            cur_user.save()
    elif step == 'giveup(1st-2)':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'포기자(1다계-2차)')
            cur_user.save()
    elif step == 'giveup(2nd)':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'포기자(2단계)')
            cur_user.save()
    elif step == 'giveup(3rd)':
        for user_id in user_list:
            cur_user = User.objects.get(id=user_id)
            cur_user.course_step = CourseStep.objects.get(title=u'포기자(3단계)')
            cur_user.save()
    else:
        return 'None'