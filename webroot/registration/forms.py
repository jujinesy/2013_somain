#-*- coding: utf-8- *-
"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""


from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from member.models import *
from member.widgets import SplitInputWidget

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    
    username = forms.CharField(label='아이디', widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    first_name = forms.CharField(label='성', widget=forms.TextInput(attrs={'class': 'input-mini'}))
    last_name = forms.CharField(label='이름', widget=forms.TextInput(attrs={'class': 'input-small'}))
    password = forms.CharField(label='비밀번호', max_length=50, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    password_confirm = forms.CharField(label='비밀번호 확인', max_length=50, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    email = forms.EmailField(label='이메일', required=False, widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    age = forms.IntegerField(label='나이', widget=forms.TextInput(attrs={'class': 'input-mini'}))
    gender = forms.ChoiceField(label='성별', choices=TYPE_GENDER_CHOICES, widget=forms.Select(attrs={
        'data-placeholder': '성별을 선택해주세요',
        'data-minimum-results-for-search': '10',
        'tabindex': '-1',
        'class': 'chzn-select span5',
        }))
    birthday = forms.DateField(label='생일', widget=forms.TextInput(attrs={'class': 'input-small'}))
    
    rr_number = forms.CharField(
        label='주민등록번호', 
        max_length=14, 
        widget=SplitInputWidget(
            number=2,
            each_attrs=[
                {'class': 'input-small', 'maxlength': '6'},
                {'class': 'input-small', 'maxlength': '7', 'password-field': True},
            ],
            
        )
    )
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
    photo = forms.ImageField(label='사진', widget=forms.ClearableFileInput)
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
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']