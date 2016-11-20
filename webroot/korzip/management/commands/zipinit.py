#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from korzip.models import Korzip, KorzipVersion
from _private import StatusBar

import re
import sys, os
import urllib, urllib2
import zipfile
import csv
import StringIO
import datetime

class Command(BaseCommand):
    args = ''
    help = '우편번호를 다운받아 데이터베이스에 삽입합니다'
    update = False

    def handle(self, *args, **options):
        if KorzipVersion.objects.get_version().strftime("%Y%m%d") != "19700101" and self.update == False:
            print "이미 우편번호 데이터가 설치되어있습니다.\n우편번호 데이터를 업데이트하려면 zipupdate를 실행해주세요."
            sys.exit()

        cursor = connection.cursor()
        cursor.execute("DELETE FROM `{0}`".format(Korzip._meta.db_table))

        page = urllib2.urlopen("http://www.zipfinder.co.kr/zipcode/").read().decode("euc-kr").encode("utf-8")
        latest_zip = re.findall(r"<a href=\"(.+)\"><font\s+face\=\"굴림\"><b>압축\(zip\) 파일<\/b><\/font><\/a>", page)[0]
        file_date = re.findall(r"(\d{8})", latest_zip)[0]

        zip_io = StringIO.StringIO()
        csv_io = StringIO.StringIO()
        zip_io.write(urllib.urlopen(latest_zip).read())

        # 압축 해제.
        zfile = zipfile.ZipFile(zip_io, "r")
        zipcodes = ""
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            if filename.find("zipcode") > -1:
                csv_io.write(zfile.read(name).decode("euc-kr").encode("utf-8"))
                csv_io.seek(0)
                break

        # CSV 파일 불러오기.
        csv_reader = csv.reader(csv_io, delimiter="\t", quotechar='"')
        arr = list(csv_reader)
        total = len(arr) - 1
        bar = StatusBar(0, total)
        print "우편번호 데이터를 {0} 테이블에 삽입합니다.\n현재 우편번호 파일버전: {1}\n새 우편번호 파일버전: {2}".format(Korzip._meta.db_table, KorzipVersion.objects.get_version().strftime("%Y%m%d"), file_date)
        bar.start()
        for row in arr:
            if row[0] != 'ZIPCODE': # 헤더는 무시하기
                try:
                    Korzip.objects.add_zip(row[0], row[1], row[2], row[3], row[4], row[5], row[6], int(row[7]))
                    bar.increment()
                except(KeyboardInterrupt, SystemExit):
                    bar.kill = True
                    sys.exit()
        KorzipVersion.objects.set_version(datetime.datetime.strptime(file_date, "%Y%m%d").date())
