#-*- coding: utf-8 -*-
from django import forms
from .models import Mail, MailContent, MailAttachment

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class MailForm(forms.Form):
    title = forms.CharField(label='제목', max_length=80, widget=forms.TextInput(attrs={ 'placeholder': '메일 제목' }))
    content = forms.CharField(label='내용', widget=forms.Textarea)
    mail_to = forms.CharField(label='수신자', widget=forms.HiddenInput(attrs={ 'readonly': 'readonly' }))
    # attachment = forms.CharField(label='첨부파일', widget=forms.HiddenInput(attrs={ 'readonly': 'readonly' }))

    def clean(self):
        self.cleaned_data = super(MailForm, self).clean()
        mail_to = self.cleaned_data.get('mail_to').split(',')

        for id in mail_to:
            if not User.objects.get(id=id):
                msg = '존재하지 않는 사용자입니다.'
                self._errors['mail_to'] = self.error_class([msg])

                del self.cleaned_data['mail_to']

        return self.cleaned_data