#-*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.db import models
#from django.utils.translation import ugettext_lazy as _



TYPE_GENDER_CHOICES = (
    ('M', '남자'),
    ('F', '여자'),
)

class Type(models.Model):
    priority = models.IntegerField(blank=True)
    visibility = models.BooleanField(default=True)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

class EducationLevel(models.Model):
    priority = models.IntegerField(blank=True)
    visibility = models.BooleanField(default=True)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

class Military(models.Model):
    priority = models.IntegerField(blank=True)
    visibility = models.BooleanField(default=True)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

# 기수
class CourseTerm(models.Model):
    priority = models.IntegerField(blank=True)
    visibility = models.BooleanField(default=True)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

# 진행 수료 탈락...등
class CourseStatus(models.Model):
    priority = models.IntegerField(blank=True)
    visibility = models.BooleanField(default=True)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

# 단계
class CourseStep(models.Model):
    priority = models.IntegerField(blank=True)
    visibility = models.BooleanField(default=True)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


import datetime

class SomaUserManager(BaseUserManager):
    def create_user(
        self,
        username,
        first_name,
        last_name,
        email,
        age,
        gender,
        birthday,
        rr_number,
        home_number,
        phone_number,
        education_level,
        military,
        photo,
        school,
        course_term,
        course_status,
        course_step,
        zipcode,
        address1,
        address2,
        google,
        twitter,
        facebook,
        type,
        password=None
    ):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            type=type,
            age=age,
            gender=gender,
            birthday=birthday,
            rr_number=rr_number,
            home_number=home_number,
            phone_number=phone_number,
            education_level=education_level,
            military=military,
            photo=photo,
            school=school,
            course_term=course_term,
            course_status=course_status,
            course_step=course_step,
            zipcode=zipcode,
            address1=address1,
            address2=address2,
            google=google,
            twitter=twitter,
            facebook=facebook,
        )

        # log = create_log(
        #     username,
        #     '1',
        #     username + ', ' + first_name + last_name + u' 회원가입',
        #     datetime.datetime.now()
        # )
        # print log
        # log.save()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        password,
        first_name='Soma',
        last_name='Admin',
        email='somain.kr@gmail.com',
        type=None,
        age=100,
        gender='M',
        birthday=datetime.datetime.now().strftime("%Y-%m-%d"),
        rr_number='111111-1111111',
        home_number='02-6933-0701',
        phone_number='02-6933-0705',
        education_level=None,
        military=None,
        photo='/static/img/logo.gif',
        school='SW Maestro',
        course_term=None,
        course_status=None,
        course_step=None,
        zipcode='135-565',
        address1='서울특별시 강남구 테헤란로',
        address2='311 아남타워빌딩',
        google='SW Maestro',
        twitter='SW Maestro',
        facebook='SW Maestro'
    ):
        # if len(Type.objects.all()) == 0:
        #     from member.management.commands import createinitialdata
        #     createinitialdata.create_type()

        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            # type=Type.objects.get(title=u'시스템 관리자'),
            type=None,
            age=age,
            gender=gender,
            birthday=birthday,
            rr_number=rr_number,
            home_number=home_number,
            phone_number=phone_number,
            education_level=None,
            military=None,
            photo=photo,
            school=school,
            course_term=None,
            course_status=None,
            course_step=None,
            zipcode=zipcode,
            address1=address1,
            address2=address2,
            google=google,
            twitter=twitter,
            facebook=facebook,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_approval = True
        user.is_receive_mail = True
        user.is_receive_staff_mail = True

        user.save(using=self._db)
        return user


class SomaUser(AbstractUser):
    # 이미 있는 것
    # username, first_name, last_name, email,
    # password, groups, user_permissions,
    # is_staff, is_active, is_superuser,
    # last_login, date_joined

    type = models.ForeignKey(Type, blank=True, null=True);
    age = models.IntegerField("나이")
    gender = models.CharField("성별", max_length=1, choices=TYPE_GENDER_CHOICES)
    birthday = models.DateField("생일")
    rr_number = models.CharField("주민등록번호", max_length=14)
    home_number = models.CharField("자택전화", max_length=14)
    phone_number = models.CharField("휴대전화", max_length=14)
    education_level = models.ForeignKey(EducationLevel, blank=True, null=True)
    military = models.ForeignKey(Military, blank=True, null=True)
    photo = models.ImageField("사진", upload_to='photo/')
    course_term = models.ForeignKey(CourseTerm, blank=True, null=True)
    course_status = models.ForeignKey(CourseStatus, blank=True, null=True)
    course_description = models.TextField("상태 사유", blank=True) # status에 대한 이유(탈퇴.등)
    course_step = models.ForeignKey(CourseStep, blank=True, null=True)

    # 우편번호
    zipcode = models.CharField("우편번호", max_length=10)
    address1 = models.CharField("주소1", max_length=100)
    address2 = models.CharField("주소2", max_length=50)

    # 선택사항
    google = models.CharField("구글 계정", max_length=100, blank=True)
    school = models.CharField("학교", max_length=100, blank=True)
    twitter = models.CharField("트위터 계정", max_length=100, blank=True)
    facebook = models.CharField("페이스북 계정", max_length=100, blank=True)

    # Push
    android_registration_id = models.CharField("GCM Registration ID", max_length=400, blank=True)

    # 권한
    '''
    기본적으로 제공되는 권한
    is_active
        자동가입을 막기 위한 메일 인증상태(django-registration)

    is_staff
        스태프 권한. 사무국 직원분들의 권한

    is_superuser
        관리자 권한. 개발자들의 권한

    추가로 정의한 권한
    is_approval
        멘티, 멘토 권한. 사무국에 의해 활동이 승인된 계정상태

    is_receive_mail
        멘티, 멘토의 경우 공지메일을 받을 지

    is_receive_staff_mail
        관리자의 경우 메일을 받을 지



    이 외에는 SomaUser의 type을 사용한다
    '''
    is_approval = models.BooleanField(default=False)
    is_receive_mail = models.BooleanField(default=True)
    is_receive_staff_mail = models.BooleanField(default=False)

    objects = SomaUserManager()

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return u'%s%s' % (self.last_name, self.first_name)

    def json(self):
        from mobile.api import convert_strftime_day

        if self is None:
            return u'None'

        return {
            'username': self.username,
            'name': self.last_name + self.first_name,
            'type': self.type.title,
            'age': self.age,
            'gender': self.gender,
            'birthday': convert_strftime_day(self.birthday),
            'photo': self.photo.url,
            'course_term': self.course_term.title,
            'course_status': self.course_status.title,
            'course_description': self.course_description,
            'course_step': self.course_step.title
        }

# 경력사항
class Career(models.Model):
    member = models.ForeignKey(SomaUser)
    title = models.CharField('근무처', max_length=100)
    start_date = models.DateField('시작날짜')
    end_date = models.DateField('종료날짜')
    description = models.TextField()

    def __unicode__(self):
        return self.title

# 수상내역
class Award(models.Model):
    member = models.ForeignKey(SomaUser)
    title = models.CharField('수상기관', max_length=100)
    date = models.DateField()
    description = models.TextField()

    def __unicode__(self):
        return self.title
