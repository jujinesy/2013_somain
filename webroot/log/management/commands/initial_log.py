#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from log.models import *

def create_type():
    # Type 생성
    print '== Type Initial data 생성시작 =='
    types = ['유저 생성', '유저 정보 수정',]
    for i in range(len(types)):
        type = types[i]
        if Type.objects.filter(title=type).exists():
            print 'Log Type : "', type, '" 은(는) 이미 있습니다'
        else:
            new_type_instance = Type(title=type)
            new_type_instance.save()
            print 'Log Type : "', type, '" 생성'
    print '== Type Initial data 생성완료 =='

class Command(BaseCommand):
    args = ''
    help = 'Log모델의 기본 데이터를 생성'

    def handle(self, *args, **options):
        create_type()