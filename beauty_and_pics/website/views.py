# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from account_app.models.accounts import *

# loading forms
from custom_form_app.forms.register_form import *
from custom_form_app.forms.login_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *

# www {{{
def www_index(request):
    return render(request, 'website/www/www_index.html', False)

def www_how_it_works(request):
    return render(request, 'website/www/www_come_funziona.html', False)

def www_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST, request)
        form.request_data=request

        # check whether it's valid:
        if form.is_valid() and form.form_actions():

		# redirect to catwalk
		return HttpResponseRedirect('/passerella/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/www/www_login.html', context)

def www_logout(request):
    logout(request)
    return render(request, 'website/www/www_index.html', False)

def www_forgot_password(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = passwordRecoverForm(request.POST, request)
        form.request_data=request

        # check whether it's valid:
        if form.is_valid() and form.form_actions():

                messages.add_message(request, messages.SUCCESS, 'Una nuova password ti è stata inviata, cambiala appena possibile nella tua area privata!')
		# redirect to catwalk
		return HttpResponseRedirect('/recupera-password/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = passwordRecoverForm()

    context = {
        "post" : request.POST,
        "form": form,
    }
    return render(request, 'website/www/www_forgot_password.html', context)

def www_register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        form.request_data=request
        # check whether it's valid:
        # if form.is_valid() and form.form_actions():
        if form.is_valid() and form.form_actions():

            # redirect to user profile
            return HttpResponseRedirect('/profilo/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/www/www_register.html', context)
# }}}

# catwalk {{{
def catwalk_index(request):
    return render(request, 'website/catwalk/catwalk_index.html', False)

def catwalk_profile(request):
    return render(request, 'website/catwalk/catwalk_profile.html', False)

def catwalk_help(request):
    return render(request, 'website/catwalk/catwalk_help.html', False)

def catwalk_report_user(request):
    return render(request, 'website/catwalk/catwalk_report_user.html', False)
# }}}

# private profile {{{
@login_required
def profile_index(request):
    return render(request, 'website/profile/profile_index.html', False)

@login_required
def profile_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AccountEditForm(request.POST)
        form.request_data=request
        # check whether it's valid:
        # if form.is_valid() and form.form_actions():
        if form.is_valid() and form.form_actions():

            messages.add_message(request, messages.SUCCESS, 'Tutte le informazioni sono state salvate correttamente')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/dati-personali/')

    # if a GET (or any other method) we'll create a blank form
    else:
	# pre-prepopulate post dictionary with current user data
	account_obj =  Account()
        request.POST = account_obj.get_autenticated_user_data(request=request)
        form = AccountEditForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/profile/profile_data.html', context)

@login_required
def profile_favorites(request):
    return render(request, 'website/profile/profile_favorites.html', False)

@login_required
def profile_stats(request):
    return render(request, 'website/profile/profile_stats.html', False)

@login_required
def profile_area51(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Area51Form(request.POST)
        # form.set_current_request(request=request)
        # check whether it's valid:
        # if form.is_valid() and form.form_actions():
        if form.is_valid() and form.form_actions():

            messages.add_message(request, messages.SUCCESS, 'Tutte le informazioni sono state salvate correttamente')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/dati-personali/')

    # if a GET (or any other method) we'll create a blank form
    else:
	# pre-prepopulate post dictionary with current user data
	account_obj =  Account()
        #request.POST = account_obj.get_autenticated_user_data(request=request)
        form = Area51Form()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/profile/profile_area51.html', context)
# }}}
