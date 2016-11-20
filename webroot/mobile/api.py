#-*- coding: utf-8 -*-
import urllib
import urllib2

# Return
from django.http import HttpResponseRedirect, HttpResponse

# Custom User model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Authenticate
from django.contrib.auth import authenticate

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# JSON Serialization
import json
from django.core import serializers

# decorator
from django.views.decorators.csrf import csrf_exempt

# datetime
from datetime import datetime, time, date

# Models
from django.forms.models import model_to_dict
from document.models import *
from structure.models import Notice, NoticeCategory


def convert_strftime_day(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    else:
        return u'None'

def convert_strftime_minute(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M')
    else:
        return u'None'

def convert_strftime_time(value):
    if isinstance(value, datetime):
        return value.strftime('%H:%M')
    else:
        return u'None'

def get_session():
    s = SessionStore()
    s.save()
    key = s.session_key
    return key

def return_failed_json():
    dict = {'return_status': 'failed'}
    return HttpResponse(json.dumps(dict), content_type='application/json')

def return_success_json():
    dict = {'return_status': 'success'}
    return HttpResponse(json.dumps(dict), content_type='application/json')


@csrf_exempt
def login(request):
    #print request
    if request.method == 'POST':
        query_dict = request.POST
        username = query_dict['username']
        password = query_dict['password']

        user = authenticate(username=username, password=password)
        #data = serializers.serialize('xml', SomeModel.objects.all(), fields=('name','size'))
        #data = serializers.serialize('json', user)

        user_data = user.json()
        data = {
            'user_data': user_data,
            }

        s = SessionStore()
        s['username'] = username
        s.save()
        session_key = s.session_key

        data['session_key'] = session_key

        return HttpResponse(json.dumps(data), content_type='application/json')


def dthandler(obj):
    #print 'start, obj:', obj.isoformat()
    if isinstance(obj, datetime):
        print 'datetime:', obj.isoformat()
        return obj.strftime('%Y-%m-%d/%H:%m')
    elif isinstance(obj, User):
        #print obj
        print 'user:', obj.isoformat()
        return obj.isoformat()
    elif hasattr(obj, 'isoformat'):
        print 'isoformat:', obj.isoformat()
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

@csrf_exempt
def document_list(request):
    if request.method == 'POST':
        query_dict = request.POST
        session_key = query_dict['session_key']
        username = query_dict['username']
        print 'username:', username

        if query_dict.has_key('type'):
            type = query_dict['type']
        else:
            type = None

        s = SessionStore(session_key=session_key)

        # request에 포함된 username과 세션에 포함된 username이 같은지 확인
        if username == s['username']:
            user = User.objects.get(username=s['username'])
        else:
            return HttpResponse('User matching invalid')

        if type == 'signed':
            documents_signed = Document.objects.filter(sign_users=user).order_by('-created')[:5]
            documents = []
            for document in documents_signed:
                if Sign.objects.filter(document=document).filter(user=user).exists():
                    documents.append(document.get_document())

        elif type == 'unsigned':
            documents_unsigned = Document.objects.filter(sign_users=user).order_by('-created')[:5]
            documents = []
            for document in documents_unsigned:
                if not Sign.objects.filter(document=document).filter(user=user).exists():
                    documents.append(document.get_document())

        #print documents
        #for doc in documents:
            #print doc
            #print '--------\n'

        data = {
            'documents': [doc.json() for doc in documents]
        }

        return HttpResponse(json.dumps(data, default=dthandler), content_type='application/json')

@csrf_exempt
def document(request):
    if request.method == 'POST':
        query_dict = request.POST
        session_key = query_dict['session_key']
        username = query_dict['username']
        document_id = int(query_dict['document_id'])

        s = SessionStore(session_key=session_key)

        if username == s['username']:
            user = User.objects.get(username=s['username'])
        else:
            return return_failed_json()

        document = Document.objects.get(id=document_id)

        return HttpResponse(json.dumps(document.json(), default=dthandler), content_type='application/json')


@csrf_exempt
def notice_list(request):
    if request.method == 'POST':
        query_dict = request.POST
        session_key = query_dict['session_key']
        username = query_dict['username']

        s = SessionStore(session_key=session_key)

        if username == s['username']:
            user = User.objects.get(username=s['username'])
        else:
            return HttpResponse('User matching invalid')

        notices = Notice.objects.all().order_by('-created')
        print notices

        data = {
            'notices': [notice.json() for notice in notices]
        }

        try:
            return HttpResponse(json.dumps(data), content_type='application/json')
        except:
            return return_failed_json()

@csrf_exempt
def sign(request):
    print '-- sign connect --'
    if request.method == 'POST':
        #print 'sign method = POST'
        try:
            query_dict = request.POST
            #print 'query_dict:', query_dict
            username = query_dict['username']
            document_id = query_dict['document_id']
            #print 'query_dict complete'
            print request.FILES
            sign_image = request.FILES['sign_image']
            #print 'debug1'

            user = User.objects.get(username=username)
            document = Document.objects.get(id=int(document_id))
            user_is_signed = document.sign_by_document.filter(user=user).exists()
            sign_users = document.sign_users.all()
            #print 'debug2'

            Sign.objects.filter(user=user, document=document).delete()
            cur_sign = Sign(user=user, document=document, image=sign_image)
            if request.FILES.has_key('photo'):
                #print 'has photo'
                photo = request.FILES['photo']
                cur_sign.photo = photo
            if query_dict.has_key('location'):
                #print 'has_location,', query_dict['location']
                location = query_dict['location']
                cur_sign.location = location
            if query_dict.has_key('wifi'):
                #print 'has_wifi'
                wifi = query_dict['wifi']
                cur_sign.wifi = wifi, query_dict['wifi']

            cur_sign.save()
            #print 'debug3'

            #print 'Document(id=', document_id, ') Signed(User=', user, ')'

            # 기부금영수증의 경우 바로 complete 및 submitted
            if isinstance(document.get_document(), DonationReceipt):
                doc = document.get_document()
                doc.is_submitted = True
                doc.is_complete = True
                doc.save()
                #print doc
                print '-- DonationReceipt Sign Complete --'
            elif isinstance(document.get_document(), MentoringReport):
                report = document.get_document()
                sign_users_length = len(report.sign_users.all())
                sign_number = len(Sign.objects.filter(document=report))
                print 'sign_users_length:', sign_users_length
                print 'sign_number:', sign_number
                #print report
                if sign_users_length == sign_number:
                    now = datetime.today()
                    report.is_complete = True
                    report.is_submitted = True
                    report.submit_time = now
                    report.save()
                    print 'MentoringReport Submitted'
                else:
                    print 'MentoringReport not submitted'
                print '-- MentoringReport Sign Complete --'

            return return_success_json()
        except:
            return return_failed_json()

@csrf_exempt
def registration_android(request):
    if request.method == 'POST':
        query_dict = request.POST
        username = query_dict['username']
        registration_id = query_dict['registration_id']

        user = User.objects.get(username=username)
        user.android_registration_id = registration_id
        user.save()

        return return_success_json()


def send_gcm(reg_id_list, data, collapse_key=None):
    print '--Start send_gcm--'
    api_key = 'AIzaSyAgMuKQvJsmPUzylZoi6at7CwX4BSqOg7U'
    data['type'] = u'normal'

    values = {
        'registration_ids': reg_id_list,
        'data': data,
    }

    values = json.dumps(values)
    print '--Set Value'

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + api_key,
        }
    print '--Set Header'

    request = urllib2.Request("https://android.googleapis.com/gcm/send", data=values, headers=headers)
    print '--Set request'
    response = urllib2.urlopen(request)
    print '--Set response'
    result = response.read()
    print '--Get result'
    print '--Result : ', result

    return result


def send_gcm_simple(reg_id_list, data, collapse_key=None):
    print '--Start send_gcm--'
    api_key = 'AIzaSyAgMuKQvJsmPUzylZoi6at7CwX4BSqOg7U'
    data['type'] = u'simple'

    values = {
        'registration_ids': reg_id_list,
        'data': data,
    }

    values = json.dumps(values)
    print '--Set Value'

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + api_key,
        }
    print '--Set Header'

    request = urllib2.Request("https://android.googleapis.com/gcm/send", data=values, headers=headers)
    print '--Set request'
    response = urllib2.urlopen(request)
    print '--Set response'
    result = response.read()
    print '--Get result'
    print '--Result : ', result

    return result
