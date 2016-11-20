#-*- coding: utf-8 -*-
from django import forms
from member.widgets import SplitInputWidget
from lectureroom.models import *

TYPE_LECTURE_CHOICES = (
    ('', '-- 선택 --'),
    ('1', '과정멘토링'),
    ('2', '집체교육'),
    ('3', '스터디'),
    ('4', '기타'),
    ('5', '자유멘토링'),
    ('6', '특강'),
)

class LectureForm(forms.Form):
    room = forms.ChoiceField(label='강의실 선택', choices=[], required=True)
    name = forms.CharField(label='회의명', max_length=30, widget=forms.TextInput(attrs={ 'placeholder': '멘토링' }), required=True)
    team = forms.CharField(label='소속', max_length=30, widget=forms.TextInput(attrs={ 'placeholder': '소프트웨어 마에스트로' }), required=False)
    count = forms.IntegerField(label='참석 인원', widget=forms.TextInput(attrs={ 'placeholder': '숫자만 입력하세요' }), required=True)
    type = forms.ChoiceField(label='사용 목적', choices=TYPE_LECTURE_CHOICES, widget=forms.Select, required=True)
    admin = forms.CharField(label='담당자명', widget=forms.TextInput(attrs={ 'placeholder': '홍길동' }), max_length=10)
    admin_tel = forms.CharField(label='담당자 연락처', widget=SplitInputWidget(number=3, each_attrs=[{ 'maxlength': 3 },{ 'maxlength': 4 },{ 'maxlength': 4 }], attrs={ 'style': 'width: 60px' }), required=True)
    message = forms.CharField(label='비고', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)
        room_choices = [('', '-- 선택 --')]
        for room in LectureRoom.objects.all():
            room_choices.append((room.id, room.name))
        self.fields['room'].choices = room_choices
