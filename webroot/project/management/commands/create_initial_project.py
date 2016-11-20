#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from project.models import Project

mentoring_types = [
    u'정규', u'자유', u'협업'
]

def create_project():
    print '\n== MentoringType모델 초기 데이터 설정 시작 ==\n'

    MentoringType.objects.all().delete()
    for project in projects:
        project_instance = Project(title=project)
        project_instance.save()

        print u'\tMentoringType :', project, u'생성되었습니다'

    print '\n== MentoringType모델 초기 데이터 설정 완료 ==\n'

class Command(BaseCommand):
    args = ''
    help = 'MentoringType의 기본데이터 모델을 생성합니다'

    def handle(self, *args, **options):
        create_project()