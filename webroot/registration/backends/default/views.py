#-*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile
from registration.views import ActivationView as BaseActivationView
from registration.views import RegistrationView as BaseRegistrationView

from structure.models import DefaultMentee, initial_default_mentee
try: default = DefaultMentee.objects.order_by('-pk')[0]
except:
    default = initial_default_mentee()

from log.models import create_log
from log.models import Type as Log_Type


class RegistrationView(BaseRegistrationView):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.
    
    """
    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """

        form_kwargs = {
            'username': cleaned_data['username'],
            'first_name': cleaned_data['first_name'],
            'last_name': cleaned_data['last_name'],
            'password': cleaned_data['password'],
            'email': cleaned_data['email'],
            'type': default.type,
            'age': cleaned_data['age'],
            'gender': cleaned_data['gender'],
            'birthday': cleaned_data['birthday'],
            'rr_number': cleaned_data['rr_number'],
            'home_number': cleaned_data['home_number'],
            'phone_number': cleaned_data['phone_number'],
            'education_level': cleaned_data['education_level'],
            'military': cleaned_data['military'],
            'photo': cleaned_data['photo'],
            'school': cleaned_data['school'],
            'course_term': default.course_term,
            'course_status': default.course_status,
            'course_step': default.course_step,
            'zipcode': cleaned_data['zipcode'],
            'address1': cleaned_data['address1'],
            'address2': cleaned_data['address2'],
            'google': cleaned_data['google'],
            'twitter': cleaned_data['twitter'],
            'facebook': cleaned_data['facebook'],
        }

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(form_kwargs, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        log_text = new_user.first_name + new_user.last_name + u' 유저가 생성되었습니다'
        log = create_log(user=new_user, 
                    type=Log_Type.objects.get(title=u'유저 생성'),
                    text=log_text
        )
        log.save()

        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('registration_complete', (), {})


class ActivationView(BaseActivationView):
    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        
        """
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):
        return ('registration_activation_complete', (), {})
