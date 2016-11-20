#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.query import QuerySet


# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from member.models import CourseTerm
from member.models import CourseStep



# project model
# circular reference발생 -> ForeignKey값을 텍스트로 입력(project.Project)
#from project.models import ProjectType, Project


'''
1. 구분(정규, 자유, 협업)
2. 프로젝트
2-1. 분과명
2-2. 기간
2-3. 지도멘토명
 -> 전부 프로젝트에 종속

3. 협업 멘토명 (구분에 종속)
4. 기수(CourseTerm) 프로젝트에 종속
5. 단계(CourseStep) 프로젝트에 종속
6. 분야(Project -> ProjectType) 프로젝트에 종속

7. 참여 연수생(다수)
8. 강의 시간(정확히 무엇?)
9. 회차(템플릿에 자동입력)
10. 날짜
11. 장소
12. 시작시간
13. 종료시간
14. 실제시간
15. 인정시간

16. 멘토링 내용-주제
16. 멘토링 내용-내용
17. 멘토링 내용-멘토의견

18. 다음일정
19. 특이사항
'''

# 새로 정의한 QuerySet
class SubClassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubClassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        else:
            return result

    def __iter__(self):
        for item in super(SubClassingQuerySet, self).__iter__():
            yield item.as_leaf_class()



# 전체 문서 베이스 모델
class Document(models.Model):
    doc_title = models.CharField(max_length=100, verbose_name='문서 제목')
    is_complete = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='문서 생성일자')
    complete_time = models.DateTimeField(blank=True, null=True, verbose_name='서명 완료시간')
    submit_time = models.DateTimeField(blank=True, null=True, verbose_name='제출시간')
    deadline = models.DateTimeField(blank=True, verbose_name='제출기한')
    sign_users = models.ManyToManyField(User, verbose_name='서명이 필요한 사용자들', related_name='document_by_sign_user', blank=True)
    submit_user = models.ForeignKey(User, verbose_name='제출한 사용자', related_name='document_by_submit_user', blank=True, null=True)
        
    def get_document(self):
        if hasattr(self, 'mentoringreport'):
            return self.mentoringreport
        elif hasattr(self, 'donationreceipt'):
            return self.donationreceipt
        elif hasattr(self, 'spendingplan'):
            return self.spendingplan
            
    def __unicode__(self):
        if hasattr(self, 'mentoringreport'):
            return self.mentoringreport.__unicode__()
        elif hasattr(self, 'donationreceipt'):
            return self.donationreceipt.__unicode__()
        elif hasattr(self, 'spendingplan'):
            return self.spendingplan.__unicode__()

    def json(self):
        from mobile.api import convert_strftime_minute, convert_strftime_time

        # 이 Document에 서명한 사용자들
        signed_users = []
        for user in self.sign_users.all():
            if Sign.objects.filter(document=self).filter(user=user).exists():
                signed_users.append(user.json())

        return {
            'id': self.id,
            'doc_type': self.doc_title,
            'is_complete': self.is_complete,
            'is_submitted': self.is_submitted,
            'created': convert_strftime_minute(self.created),
            'complete_time': convert_strftime_minute(self.complete_time),
            'submit_time': convert_strftime_minute(self.submit_time),
            'deadline': convert_strftime_minute(self.deadline),
            'sign_users': [user.json() for user in self.sign_users.all()],
            'signed_users': signed_users,
            'submit_user': self.submit_user.json() if self.submit_user is not None else u'None'
        }


# 서명정보
class Sign(models.Model):
    user = models.ForeignKey(User, related_name='sign_by_user')
    document = models.ForeignKey(Document, related_name='sign_by_document')
    image = models.ImageField(upload_to='sign/', blank=True, null=True)
    photo = models.ImageField(upload_to='sign_photo/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    wifi = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s%s - %s, %s' % (self.user.last_name, self.user.first_name, self.document, self.created)


# 정규, 자유, 협업
class MentoringType(models.Model):
    title = models.CharField("구분", max_length=100)

    def __unicode__(self):
        return self.title

class MentoringReport(Document):
    type = models.ForeignKey(MentoringType, verbose_name='구분')
    project = models.ForeignKey('project.Project', verbose_name='프로젝트', related_name='mentoring_report_by_project')
    mentor = models.ForeignKey(User, blank=True, null=True, verbose_name='멘토', related_name='cooperation_mentor')
    is_cooperation = models.BooleanField(default=False, verbose_name='협업 멘토링 여부')
    
    mentees = models.ManyToManyField(User, verbose_name='참여 연수생')
    date = models.DateField(verbose_name='멘토링 날짜')
    place = models.CharField(max_length=100, verbose_name='장소')
    start_time = models.TimeField(verbose_name='시작 시간')
    end_time = models.TimeField(verbose_name='종료 시간')

    real_time = models.TimeField(blank=True)
    accept_time = models.TimeField(blank=True)

    title = models.CharField(max_length=100, verbose_name='주제')
    content = models.TextField(verbose_name='내용')
    opinion = models.TextField(verbose_name='멘토 의견', blank=True)

    schedule = models.TextField(verbose_name='다음 일정', blank=True)
    issue = models.TextField(verbose_name='특이사항', blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.date, self.project)

    def get_strftime_real():
        minute = self.real_time
        hour = 0
        while minute >= 60:
            hour = hour + 1
            minute = minute - 60

        return '%s:%s' % (str(hour).zfill(2), str(minute).zfill(2))

    def get_strftime_accept():
        minute = self.accept_time
        hour = 0
        while minute >= 60:
            hour = hour + 1
            minute = minute - 60

        return '%s:%s' % (str(hour).zfill(2), str(minute).zfill(2))

    def save(self, *args, **kwargs):
        self.doc_title = u'멘토링 보고서'
        super(Document, self).save(*args, **kwargs)

    def json(self):
        from mobile.api import convert_strftime_minute, convert_strftime_time

        document_dict = self.document_ptr.json()
        #print 'document_dict:', document_dict
        if self.mentor is None:
            mentor_value = u'None'
        else:
            mentor_value = self.mentor.json()

        cur_dict = {}
        # title 뽑아야 하는 변수
        for key in ['type', 'project']:
            cur_dict[key] = getattr(self, key).title

        # 시간 뽑아야 하는 변수
        for key in ['date', 'start_time', 'end_time', 'real_time', 'accept_time']:
            if key == 'date':
                cur_dict[key] = convert_strftime_minute(getattr(self, key))
            else:
                cur_dict[key] = convert_strftime_time(getattr(self, key))

        # 그냥 꺼내는 변수
        for key in ['is_cooperation', 'title', 'content', 'opinion', 'schedule', 'issue']:
            cur_dict[key] = getattr(self, key)

        # User 변수
        cur_dict['mentor'] = self.mentor.json() if self.mentor is not None else u'None'
        cur_dict['mentee'] = [mentee.json() for mentee in self.mentees.all()]

        combine_dict = {
            'document': document_dict,
            'extends': cur_dict,
        }
        return combine_dict

class SpendingPlan(Document):
    title = models.CharField(max_length=100, verbose_name='주제')

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.doc_title = u'지출 계획서'
        super(Document, self).save(*args, **kwargs)

class DonationReceipt(Document):
    year = models.IntegerField(verbose_name='연도')
    month = models.IntegerField(verbose_name='월')
    address = models.CharField(max_length=200, blank=True, verbose_name='주소')

    def user(self):
        return self.sign_users.all()[0]

    def __unicode__(self):
        user = self.sign_users.all()[0]
        return u'%d년 %d월 기부금영수증 (%s%s)' % (self.month, self.month, user.last_name, user.first_name)

    def save(self, *args, **kwargs):
        self.doc_title = u'기부금 영수증'
        super(Document, self).save(*args, **kwargs)

    def json(self):
        document_dict = self.document_ptr.json()
        #print 'document_dict:', document_dict

        cur_dict = {
            'year': self.year,
            'month': self.month,
        }

        combine_dict = {
            'document': document_dict,
            'extends': cur_dict,
        }
        return combine_dict