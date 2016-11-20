#-*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# python library
from nptime import nptime
import calendar
from calendar import monthrange
from datetime import datetime, timedelta
from datetime import time as dt_time
from datetime import date as dt_date
from dateutil.relativedelta import relativedelta
import time

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from document.models import *
from document.forms import DonationReceiptForm

def create_donationreceipt(request):
    if request.method == 'POST':
        form = DonationReceiptForm(request.POST, initial={})

        if form.is_valid():
            print form.cleaned_data
            mentees = User.objects.filter(type__title=u'멘티')

            obj = form.save(commit=False)
            for mentee in mentees:
                obj.save()
                obj.sign_users.add(mentee)
                obj.save()

                # GCM 전송
                from mobile.api import send_gcm
                reg_id_list = [user.android_registration_id for user in obj.sign_users.all()]
                data = {
                    'document': obj.json(),
                }
                send_gcm(reg_id_list, data)

                obj.pk = None
                obj.id = None

                print u'기부금영수증 / %s%s' % (mentee.last_name, mentee.first_name)

            return redirect('document:index')
        else:
            return render('manager/document/donationreceipt/create.html', {'form': form}, RequestContext(request))
    else:
        form = DonationReceiptForm
        dict = {
            'form': form,
        }
        return render_to_response('manager/document/donationreceipt/create.html', dict, RequestContext(request))

def donationreceipt_report(request):
    def add_month(sourcedate, months):
         month = sourcedate.month - 1 + months
         year = sourcedate.year + month / 12
         month = month % 12 + 1
         day = min(sourcedate.day, calendar.monthrange(year, month)[1])
         return dt_date(year, month, day)

    today_min = datetime.combine(datetime.today(), dt_time.min)
    today_max = datetime.combine(datetime.today(), dt_time.max)
    d = {}

    d['target'] = target = datetime(int(request.GET.get('y', datetime.today().year)), int(request.GET.get('m', datetime.today().month)), 1)
    # last_month = datetime(month.year, month.month, monthrange(month.year, month.month)[1])
    # d['min_date'] = min_date = datetime.combine(month, dt_time.min)
    # d['max_date'] = max_date = datetime.combine(last_month, dt_time.max)
    d['prev_date'] = prev_date = add_month(target, -1)
    d['next_date'] = next_date = add_month(target, 1)

    d['submitted'] = submitted = DonationReceipt.objects.filter(year=target.year, month=target.month, is_submitted=True)
    d['not_submitted'] = not_submitted = DonationReceipt.objects.filter(year=target.year, month=target.month, is_submitted=False)

    return render_to_response('manager/document/donationreceipt/report.html', d)
