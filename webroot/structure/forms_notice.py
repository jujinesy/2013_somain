from django.forms import ModelForm
from django import forms

from structure.models import Notice, NoticeCategory

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

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice

        widgets = {
            'title': forms.TextInput(attrs=textinput_xxlarge),
            'content': forms.Textarea(attrs=textarea_big),
        }

class NoticeCategoryForm(forms.ModelForm):
    class Meta:
        model = NoticeCategory

        widgets = {
            'title': forms.TextInput(attrs=textinput_xxlarge),
        }