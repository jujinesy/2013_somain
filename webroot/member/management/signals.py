#-*- coding: utf-8 -*-
from django.db.models.signals import post_syncdb
from member.models import *
import member.models

TYPE_TYPE_CHOICES = (
    ('1', u'멘티'),
    ('2', u'멘토'),
    ('3', u'관리자'),
    ('4', u'시스템 관리자'),
)
TYPE_EDU_CHOICES = (
    ('1', u'고등학교 재학'),
    ('2', u'고등학교 졸업'),
    ('3', u'대학교 재학'),
    ('4', u'대학교 졸업'),
    ('5', u'대학원 재학'),

    ('20', u'해당없음'),
)
TYPE_MILITARY_CHOICES = (
    ('1', u'면제'),
    ('2', u'미필'),
    ('3', u'군필'),

    ('20', u'해당없음'),
)
TYPE_COURSE_TERM_CHOICES = (
    ('1', u'1기'),
    ('2', u'2기'),
    ('3', u'3기'),
    ('4', u'4기'),
    ('5', u'5기'),
    ('6', u'6기'),
    ('7', u'7기'),

    ('20', u'해당없음'),
)
TYPE_COURSE_STATUS_CHOICES = (
    ('1', u'진행'),
    ('2', u'수료'),
    ('3', u'탈락'),
    ('4', u'포기'),

    ('20', u'해당없음'),
)
TYPE_COURSE_STEP_CHOICES = (
    ('1-1', u'1단계-1차'),
    ('1-2', u'1단계-2차'),
    ('2', u'2단계'),
    ('3', u'3단계'),

    ('11', u'인증자'),
    ('12', u'포기자(1단계-1차)'),
    ('13', u'포기자(1단계-2차)'),
    ('14', u'포기자(2단계)'),
    ('15', u'포기자(3단계)'),

    ('20', u'해당없음'),
)

CHOICES = {
    'type' : {
        'title': 'Type',
        'model': Type,
        'choice': TYPE_TYPE_CHOICES
    },
    'edu' : {
        'title': 'EducationLevel',
        'model': EducationLevel,
        'choice': TYPE_EDU_CHOICES
    },
    'military' : {
        'title': 'Military',
        'model': Military,
        'choice': TYPE_MILITARY_CHOICES
    },
    'courseterm' : {
        'title': 'CourseTerm',
        'model': CourseTerm,
        'choice': TYPE_COURSE_TERM_CHOICES
    },
    'coursestatus' : {
        'title': 'CourseStatus',
        'model': CourseStatus,
        'choice': TYPE_COURSE_STATUS_CHOICES
    },
    'coursestep' : {
        'title': 'CourseStep',
        'model': CourseStep,
        'choice': TYPE_COURSE_STEP_CHOICES
    }
}

def create_initial_data():
    print '== Member모델 초기 데이터 설정 시작 =='
    for i in range(len(CHOICES.keys())):
        key = CHOICES.keys()[i]
        d = CHOICES[key]

        type_title = d['title']
        model = d['model']
        choice = d['choice']

        #전체 삭제
        model.objects.all().delete()

        for j in range(len(choice)):
            number, title = choice[j]
            if model.objects.filter(title=title).exists():
                print type_title, ':', title, u'은(는) 이미 있습니다'
            else:
                new_instance = model(priority=i, title=title)
                new_instance.save()
                print type_title, ':', title, '생성되었습니다'
    print '== Member모델 초기 데이터 설정 완료 =='


def syncdb_callback(sender, **kwargs):
    create_initial_data()

# post_syncdb.connect(syncdb_callback, sender=member.models)
