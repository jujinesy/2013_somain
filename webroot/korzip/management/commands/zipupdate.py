#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from korzip.models import KorzipVersion
from korzip.management.commands.zipinit import Command as initCommand

import re
import urllib, urllib2
import sys
import datetime

class Command(BaseCommand):
    args = ''
    help = '우편번호 데이터를 업데이트합니다'

    def handle(self, *args, **options):
        korzip_version = KorzipVersion.objects.get_version()
        if korzip_version.strftime("%Y%m%d") == "19700101":
            print "우편번호 데이터가 없습니다.\nzipinit를 먼저 실행해주세요."
            sys.exit()

        print "최신 우편번호 데이터가 있는지 확인합니다."
        page = urllib2.urlopen("http://www.zipfinder.co.kr/zipcode/").read().decode("euc-kr").encode("utf-8")
        latest_zip = re.findall(r"<a href=\"(.+)\"><font\s+face\=\"굴림\"><b>압축\(zip\) 파일<\/b><\/font><\/a>", page)[0]
        latest_version = datetime.datetime.strptime(re.findall(r"(\d{8})", latest_zip)[0], "%Y%m%d").date()

        # 최신버전이 존재할 경우
        if latest_version > korzip_version:
            print "최신버전이 존재합니다. 업데이트를 진행합니다.\n\033[91m주의: 업데이트를 강제로 중단시킬 경우 우편번호 데이터가 모두 들어가지 않습니다.\033[0m"
            init_command = initCommand()
            init_command.update = True
            init_command.handle(args, options)
        else:
            print "현재 우편번호 데이터(%s)는 최신 데이터입니다." % (korzip_version.strftime("%Y%m%d"))
            sys.exit()
