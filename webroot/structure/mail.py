#-*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# 관리자 메일 보내기(제목, 내용만)
def send_staff(subject, message):
    user_list = User.objects.filter(is_receive_staff_mail=True)
    user_email_list = []
    for user in user_list:
        user_email_list.append(user.email)
    
    send_mail(subject, message, 'somain.kr@gmail.com', user_email_list)

# 메일 발송 테스트 뷰
def send_staff_view(request):
    send_staff('Test Subject', 'Test Message')

    return HttpResponse('Mail Test')