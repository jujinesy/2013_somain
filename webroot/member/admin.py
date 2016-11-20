#-*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from member.models import SomaUser, Career, Award

class SomaUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()

class SomaUserCreationForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
            raise forms.ValidationError(self.error_messages['duplicate_username'])

class SomaUserAdmin(UserAdmin):
    form = SomaUserChangeForm
    add_form = SomaUserCreationForm
    fieldsets = (
        (None,              {'fields': ('username', 'password',)}),
        ('Personal info',   {'fields': ('first_name', 'last_name', 'email',)}),
    )


admin.site.register(SomaUser)
admin.site.register(Award)

# admin.site.register(Log)
admin.site.unregister(Group)