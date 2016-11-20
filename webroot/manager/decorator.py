#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect

# 스태프권한 decorator
def staff_login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.is_staff == True:
                return function(request, *args, **kwargs)
            else:
                return redirect('manager:only_admin')
        else:
            return redirect('/admin/login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap