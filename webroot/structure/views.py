#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.shortcuts import HttpResponse
from django.template import RequestContext
from registration.forms import RegistrationForm

from structure.models import Notice
from lectureroom.models import Lecture
from member.forms import SomaUserEditForm

from datetime import datetime

# Log
from log.models import create_log
from log.models import Type as Log_Type

def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user

        # anonymous유저가 아니고, is_apporval인 유저일 때 진행
        if user.is_anonymous():
            return render_to_response('index.html', RequestContext(request))

        elif not user.is_approval:
            return render_to_response('structure/required_approval.html', RequestContext(request))

        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

@login_required
def main(request):
    user = request.user
    require_sign_documents = []

    docs = user.document_by_sign_user.filter(is_complete=False)
    for doc in docs:
        if doc.sign_by_document.filter(user=user).exists():
            pass
        else:
            require_sign_documents.append(doc)

    d = {
        'user': user,
        'hide_title_bar': True,
        'notice': Notice.objects.all().order_by('-created')[:10],
        'req_sign_docs': require_sign_documents,
        'lectures': Lecture.objects.filter(start__lte=datetime.now()).order_by('-end')[:5],
    }
    return render_to_response('dashboard.html', d, RequestContext(request))

# database signal hook
@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = SomaUserEditForm(request.POST, request.FILES)

        if form.is_valid():
            data = {}
            data['email'] = form.cleaned_data['email']
            data['home_number'] = form.cleaned_data['home_number']
            data['phone_number'] = form.cleaned_data['phone_number']
            data['education_level'] = form.cleaned_data['education_level']
            data['military'] = form.cleaned_data['military']
            data['school'] = form.cleaned_data['school']
            data['zipcode'] = form.cleaned_data['zipcode']
            data['address1'] = form.cleaned_data['address1']
            data['address2'] = form.cleaned_data['address2']
            data['google'] = form.cleaned_data['google']
            data['twitter'] = form.cleaned_data['twitter']
            data['facebook'] = form.cleaned_data['facebook']

            # 유저정보 변경, data와 user의 기존값차이를 log남기기
            log_text = u'프로필 변경'
            for k in data.keys():
                # 클래스의 
                user_value = getattr(user, k)

                if user_value != data[k]:
                    print str(user_value)
                    print str(data[k])
                    print type(str(user_value))
                    print type(str(data[k]))
                    print '--'
                    log_text = log_text + str(user_value).decode('utf-8') + str(data[k]).decode('utf-8')
                    setattr(user, k, data[k])

            # 로그생성
            log_type, exist = Log_Type.objects.get_or_create(title=u'유저 정보 수정')
            log = create_log(user=request.user,
                            type=log_type,
                            text=log_text)
            log.save()

            # 변경된 유저정보 저장
            user.save()


            # return HttpResponse("Edit Profile")
            return redirect('edit_profile')
        else:
            # print form.errors
            # print form.cleaned_data
            form = SomaUserEditForm(request.POST, request.FILES)
    else:
        form = SomaUserEditForm(instance=user)

    return render_to_response('structure/edit_profile.html', {'form': form, 'user': user,}, RequestContext(request))
