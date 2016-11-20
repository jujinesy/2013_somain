#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from log.models import Type

class Command(BaseCommand):
    args = ''
    help = 'Log의 Type모델 종류를 보여줌'

    def handle(self, *args, **options):
        for type in Type.objects.all():
            print type