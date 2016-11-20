#-*- coding: utf-8 -*-
from django.db import models
import datetime

class KorzipManager(models.Manager):
    def add_zip(self, zipcode, sido, gungu, dong, ri, bldg, bunji, seq):
        zip = self.model(
            zipcode=zipcode,
            sido=sido,
            gungu=gungu,
            dong=dong,
            ri=ri,
            bldg=bldg,
            bunji=bunji,
            seq=seq,
        )
        zip.save()
        return zip

class KorzipVersionManager(models.Manager):
    def get_version(self):
        if super(KorzipVersionManager, self).count() == 0:
            return datetime.date(1970, 01, 01)
        else:
            return super(KorzipVersionManager, self).get(id=1).version

    def set_version(self, version):
        if super(KorzipVersionManager, self).count() == 0:
            self.model(
                version=version
            ).save()
        else:
            data = super(KorzipVersionManager, self).get(id=1)
            data.version = version
            data.save()

class Korzip(models.Model):
    zipcode = models.CharField("우편번호", max_length=7, db_index=True)
    sido = models.CharField("특별시,광역시,도", max_length=4, blank=True)
    gungu = models.CharField("시,군,구", max_length=17, blank=True)
    dong = models.CharField("읍,면,동", max_length=26, blank=True, db_index=True)
    ri = models.CharField("리", max_length=15, blank=True)
    bldg = models.CharField("건물명", max_length=42, blank=True, db_index=True)
    bunji = models.CharField("번지수", max_length=17, blank=True)
    seq = models.IntegerField("데이터 순서", db_index=True)
    
    objects = KorzipManager()

class KorzipVersion(models.Model):
    version = models.DateField("파일 버전")

    objects = KorzipVersionManager()
