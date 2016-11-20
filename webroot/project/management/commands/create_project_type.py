#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from project.models import * 

project_types = [
    (u'개발기획', u'개발기획 Description'),
    ('Web', 'Web Description'),
    ('SE/SI', 'SE/SI Description'),
    ('Architecture', 'Architecture Description'),
    ('Mobile', 'Mobile Description'),
    ('Embedded', 'Embedded Description'),
    ('OS', 'OS Description'),
    (u'보안', u'보안 Description'),
    ('DB', 'DB Description'),
    ('Game', 'Game Description'),
    (u'SW 품질관리', u'SW 품질관리 Description'),
    ('UX/UI', 'UX/UI Description')
]



def create_project_type():
    print '\n== ProjectType모델 초기 데이터 설정 시작 ==\n'

    ProjectType.objects.all().delete()
    for project_type in project_types:
        title, desc = project_type
        
        project_type_instance = ProjectType(title=title, content=desc)
        project_type_instance.save()

        print u'\tProjectType :', title, u'생성되었습니다'

    print '\n== ProjectType모델 초기 데이터 설정 완료 ==\n'

class Command(BaseCommand):
    args = ''
    help = 'Member모듈의 기수와 타입.등의 기본데이터 모델을 생성합니다'

    def handle(self, *args, **options):
        create_project_type()