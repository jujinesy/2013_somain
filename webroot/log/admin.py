#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from log.models import Log

admin.site.register(Log)