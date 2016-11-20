#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from project.models import *
from document.models import MentoringReport
from document.models import DonationReceipt

from django.contrib.admin import widgets


textinput_mini = {
    'class': 'input-mini',
}
textinput_small = {
    'class': 'input-small',
}
textinput_large = {
    'class': 'input-large',
}
textinput_xlarge = {
    'class': 'input-xlarge',
}
textinput_xxlarge = {
    'class': 'input-xxlarge',
}

textarea_big = {
    'class': 'span8',
    'rows': 10,
}
textarea_mid = {
    'class': 'span8',
    'rows': 5,
}
textarea_small = {
    'class': 'span8',
    'rows': 3,
}
select = {
    'class': "chzn-select",
}
class MentoringReportForm(forms.ModelForm):

    class Meta:
        model = MentoringReport
        exclude = ['mentor', 'project', 'doc_title', 'is_complete', 'complete_time', 'submit_time', 'is_submitted', 'sign_users', 'submit_user', 'deadline', 'real_time', 'accept_time']

        widgets = {
            'type': forms.RadioSelect(),
            'mentees': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs=textinput_xxlarge),
            'content': forms.Textarea(attrs=textarea_big),
            'opinion': forms.Textarea(attrs=textarea_mid),
            'schedule': forms.Textarea(attrs=textarea_small),
            'issue': forms.Textarea(attrs=textarea_small),
        }

class DonationReceiptForm(forms.ModelForm):

    class Meta:
        model = DonationReceipt
        exclude = ['doc_title', 'is_complete', 'complete_time', 'submit_time', 'is_submitted', 'sign_users', 'submit_user', 'user', 'address']

        widgets = {
            'year': forms.TextInput(attrs=textinput_mini),
            'month': forms.TextInput(attrs=textinput_mini),
        }