#-*- coding: utf-8 -*-
from django.db import models
from django.utils.html import format_html, mark_safe

from member.models import Type as MemberType
from member.models import CourseTerm, CourseStatus, CourseStep

# 회원가입시 기본 설정값
class DefaultMentee(models.Model):
    type = models.ForeignKey(MemberType)
    course_term = models.ForeignKey(CourseTerm)
    course_status = models.ForeignKey(CourseStatus)
    course_step = models.ForeignKey(CourseStep)

    def __unicode__(self):
        text = u'%s %s %s' % (self.type.title, self.course_term.title, self.course_status.title, self.course_step.title)
        return text

def initial_default_mentee():
    instance = DefaultMentee(
        type=MemberType.objects.get(title=u'멘티'),
        course_term=CourseTerm.objects.get(title=u'4기'),
        course_status=CourseStatus.objects.get(title=u'해당없음'),
        course_step=CourseStep.objects.get(title=u'해당없음')
    )
    instance.save()
    return instance


class NoticeCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='카테고리 이름')
    priority = models.IntegerField(default=0, verbose_name='우선순위')

    def __unicode__(self):
        return u'공지사항 카테고리(%s)' % (self.title)

# 공지사항
class Notice(models.Model):
    is_important = models.BooleanField(default=False, verbose_name='최상단 표시')
    category = models.ForeignKey(NoticeCategory, verbose_name='카테고리')
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(blank=True, verbose_name='내용')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일자')

    def __unicode__(self):
        return u'공지사항 : %s / %s' % (self.category.title, self.title)

    def json(self):
        from mobile.api import convert_strftime_minute, convert_strftime_time, convert_strftime_day

        dict = {
            'return_status': 'success',
            'is_important': self.is_important,
            'category': self.category.title,
            'title': self.title,
            'content': mark_safe(self.content).replace('\r\n', '<br/>'),
            'created_day': convert_strftime_day(self.created),
            'created_time': convert_strftime_time(self.created),
        }

        return dict