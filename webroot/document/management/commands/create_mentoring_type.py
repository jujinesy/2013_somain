#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from document.models import MentoringType

mentoring_types = [
    u'정규', u'자유', u'협업'
]

def create_mentoring_type():
    print '\n== MentoringType모델 초기 데이터 설정 시작 ==\n'

    MentoringType.objects.all().delete()
    for mentoring_type in mentoring_types:
        mentoring_type_instance = MentoringType(title=mentoring_type)
        mentoring_type_instance.save()

        print u'\tMentoringType :', mentoring_type, u'생성되었습니다'

    print '\n== MentoringType모델 초기 데이터 설정 완료 ==\n'

class Command(BaseCommand):
    args = ''
    help = 'MentoringType의 기본데이터 모델을 생성합니다'

    def handle(self, *args, **options):
        create_mentoring_type()