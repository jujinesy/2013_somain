#-*- coding: utf-8 -*-
from django.db import models
# from django.contrib.auth.models import User

# # Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# member model
from member.models import CourseTerm, CourseStep

'''
Web, DB 등등...
'''
class ProjectType(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __unicode__(self):
        return self.title

class Project(models.Model):
    type = models.ForeignKey(ProjectType, related_name='project_by_project_type')
    title = models.CharField(max_length=100)
    mentor = models.ForeignKey(User, related_name='project_by_mentor')
    mentees = models.ManyToManyField(User, related_name='project_by_mentees')

    course_term = models.ForeignKey(CourseTerm, related_name='project_by_course_term')
    course_step = models.ForeignKey(CourseStep, related_name='project_by_course_step')

    # 완료된 프로젝트인지
    is_finished = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s | %s%s 멘토' % (self.title, self.mentor.last_name, self.mentor.first_name)