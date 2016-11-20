#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from member.models import *
from member.widgets import SplitInputWidget

class SomaUserEditForm(forms.ModelForm):
    #username=forms.CharField(label='아이디')
    #first_name=forms.CharField(label='성')
    #last_name=forms.CharField(label='이름')
    #age=forms.CharField(label='나이')
    #gender=forms.CharField(label='성별')
    #birthday=forms.CharField(label='생일')
    #rr_number=forms.CharField(label='주민등록번호')
    email = forms.EmailField(label='이메일', required=False, widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    home_number = forms.CharField(
        label='집 전화번호',
        max_length=14,
        widget=SplitInputWidget(
            number=3,
            each_attrs=[
                {'class': 'input-mini', 'maxlength': '4'},
                {'class': 'input-mini', 'maxlength': '4'},
                {'class': 'input-mini', 'maxlength': '4'},
            ],

        )
    )
    phone_number = forms.CharField(
        label='휴대전화 번호',
        max_length=14,
        widget=SplitInputWidget(
            number=3,
            each_attrs=[
                {'class': 'input-mini', 'maxlength': '4'},
                {'class': 'input-mini', 'maxlength': '4'},
                {'class': 'input-mini', 'maxlength': '4'},
            ],

        )
    )

    education_level = forms.ModelChoiceField(label='학력', queryset=EducationLevel.objects.all(), widget=forms.Select(attrs={
        'data-placeholder': '학력을 선택해주세요',
        'data-minimum-results-for-search': '10',
        'tabindex': '-1',
        'class': 'chzn-select span5',
        }))
    military = forms.ModelChoiceField(label='병역사항', queryset=Military.objects.all(), widget=forms.Select(attrs={
        'data-placeholder': '병역상태를 선택해주세요',
        'data-minimum-results-for-search': '10',
        'tabindex': '-1',
        'class': 'chzn-select span5',
        }))
    # photo = forms.ImageField(label='사진', widget=forms.ClearableFileInput())
    school = forms.CharField(label='학교명', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # 우편번호
    zipcode = forms.CharField(label='우편번호', max_length=7, widget=SplitInputWidget(
        number=2,
        each_attrs=[
            {'readonly': 'readonly', 'class': 'input-mini'},
            {'readonly': 'readonly', 'class': 'input-mini'}
        ]
    ))
    address1 = forms.CharField(label='주소1', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address2 = forms.CharField(label='주소2', max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    # 선택사항
    google = forms.CharField(label='구글 계정', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    twitter = forms.CharField(label='트위터 계정', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    facebook = forms.CharField(label='페이스북 계정', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = SomaUser
        # Validation 에서 제외할 항목
        exclude = ['username', 'first_name', 'last_name', 'age', 'gender', 'birthday', 'rr_number', 'photo',
                   'course_description', 'course_status', 'last_login', 'course_step', 'date_joined', 'password', 'type', 'course_term']


class AwardForm(forms.Form):
    title = forms.CharField(label='제목', max_length=100, widget=forms.TextInput())
    date = forms.DateField(label='시작날짜', widget=forms.TextInput())
    description = forms.CharField(label='상세정보', widget=forms.Textarea())

class CareerForm(forms.Form):
    title = forms.CharField(label='제목', max_length=100, widget=forms.TextInput())
    start_date = forms.DateField(label='시작일자', widget=forms.TextInput())
    end_date = forms.DateField(label='종료일자', widget=forms.TextInput())
    description = forms.CharField(label='상세정보', widget=forms.Textarea())
