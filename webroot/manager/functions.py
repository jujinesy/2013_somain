#-*- coding: utf-8 -*-

# 분 단위를 받아 00:00 형태로 출력
def get_strftime(minute):
    hour = 0
    while minute >= 60:
        hour = hour + 1
        minute = minute - 60

    return '%s:%s' % (str(hour).zfill(2), str(minute).zfill(2))