#-*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

TYPE_LECTURE_CHOICES = (
    ('1', '과정멘토링'),
    ('2', '집체교육'),
    ('3', '스터디'),
    ('4', '기타'),
    ('5', '자유멘토링'),
    ('6', '특강'),
)

# TYPE_ROOM_CHOICES = (
#     ('1', '아남타워 [기타]'),
#     ('2', '연수센터 7층 [해찬1]'),
#     ('3', '연수센터 7층 [해찬2]'),
#     ('4', '연수센터 7층 [해찬3]'),
#     ('5', '연수센터 2층 [아람2-1]'),
#     ('6', '연수센터 2층 [아람2-2]'),
#     ('7', '연수센터 2층 [아람2-3]'),
#     ('8', '연수센터 7층 [아람7-6]'),
#     ('9', '연수센터 7층 [아람7-5_3기 3단계]'),
#     ('10', '연수센터 7층 [아람7-4_3기 3단계]'),
#     ('11', '연수센터 7층 [아람7-7]'),
#     ('12', '연수센터 2층 [커뮤니티]'),
#     ('13', '연수센터 7층 [아람7-3_3기 3단계]'),
#     ('14', '연수센터 7층 [아람7-2_3기 3단계]'),
#     ('15', '연수센터 7층 [아람7-1_3기 3단계]'),
# )
class LectureRoom(models.Model):
    name = models.CharField('강의실 이름', max_length=50)

    def get_name(self):
        return self.name

class LectureBlockManager(models.Manager):
    def new_block(self, name, content, start_date, end_date, room):
        block = self.model(
                name=name,
                content=content,
                start_date=start_date,
                end_date=end_date,
                room=room,
            )
        block.save()
        return block

class LectureBlock(models.Model):
    name = models.CharField('차단 제목', max_length=100)
    content = models.TextField('차단 사유')
    start_date = models.DateTimeField('시작일시', blank=True, db_index=True)
    end_date = models.DateTimeField('종료일시', blank=True, db_index=True)
    room = models.ForeignKey(LectureRoom)

    objects = LectureBlockManager()

class LectureManager(models.Manager):
    def new_lecture(self, user, team, name, room, count, xtype, start, end, admin, admin_tel, message):
        result = {
            'success': False,
            'data': '',
        }

        # 강의실이 차단된(Blocked) 강의실인지 먼저 확인한다.
        '''
            지정된 강의실이:
                1. start 가 start_date 와 end_date 사이에 있을 경우
                2. end 가 start_date 와 end_date 사이에 있을 경우
        '''
        check = self.check_lecture(room, start, end)
        if type(check) != bool:
            return result
        else:
            lecture = self.model(
                user=user,
                team=team,
                name=name,
                room=room,
                count=count,
                type=xtype,
                start=start,
                end=end,
                admin=admin,
                admin_tel=admin_tel,
                message=message,
            )
            lecture.save()
            if lecture:
                result['success'] = True
                result['data'] = lecture
            return result

    def check_lecture(self, room, start, end):
        block = LectureBlock.objects.filter(Q(Q(start_date__range=(start, end)) | Q(end_date__range=(start, end)) | Q(start_date__lte=start, end_date__gte=end)), room=room)
        exist = super(LectureManager, self).filter(Q(Q(start__range=(start, end)) | Q(end__range=(start, end)) | Q(start__lte=start, end__gte=end)), room=room)
        print block

        if block.count() > 0:
            return block
        elif exist.count() > 0:
            return exist
        else:
            return True

    def remove_lecture(self):

        return False

    def get_lecture(self, start, end):
        result = {
            'count': 0,
            'data': [],
        }

        lectures = super(LectureManager, self).filter(start__gte=start, end__lte=end)
        for lecture in lectures:
            result['count'] += 1
            result['data'].append(lecture)

        return result

class Lecture(models.Model):
    user = models.ForeignKey(User)
    team = models.CharField('소속', max_length=30)
    name = models.CharField('회의명', max_length=30)
    room = models.ForeignKey(LectureRoom)
    count = models.IntegerField('참석 인원')
    type = models.CharField('사용 목적', max_length=1, choices=TYPE_LECTURE_CHOICES)
    start = models.DateTimeField('시작일시', db_index=True)
    end = models.DateTimeField('종료일시', db_index=True)
    admin = models.CharField('담당자명', max_length=10)
    admin_tel = models.CharField('담당자 연락처', max_length=12)
    message = models.TextField('비고')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LectureManager()
