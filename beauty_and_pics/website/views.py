# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from account_app.models.accounts import *
from contest_app.models.contests import *
from contest_app.models.votes import Vote
# loading forms
from custom_form_app.forms.register_form import *
from custom_form_app.forms.login_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from custom_form_app.forms.help_request_form import *
from custom_form_app.forms.upload_book_form import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# www {{{
def www_index(request):
    # TODO: debug only, plz remove
    Contest_obj = Contest()
    Contest_obj.get_active_contests_end_time()
    Contest_obj.get_opening_contests_start_time()
    return render(request, 'website/www/www_index.html', False)

def www_how_it_works(request):
    return render(request, 'website/www/www_come_funziona.html', False)

def www_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        form.set_current_request(request=request)

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
        form = passwordRecoverForm(request.POST)
        form.set_current_request(request=request)

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
        form.set_current_request(request=request)

        # check whether it's valid:
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
@ensure_csrf_cookie
def catwalk_index(request):
    return render(request, 'website/catwalk/catwalk_index.html', False)

@ensure_csrf_cookie
def catwalk_profile(request, user_id):
    # retrieve user info
    account_obj =  Account()
    account_info = account_obj.custom_user_id_data(user_id=user_id)

    # retrieve contest user info
    contest_account_info = account_obj.get_contest_account_info(user_id=user_id)

    # TODO: put this inside a middleware
    top_five_account = account_obj.get_top_five_contest_user()

    # check if this catwalker can be voted
    vote_obj = Vote()
    user_already_voted = False
    try:
        vote_obj.check_if_user_can_vote(user_id=user_id, ip_address=request.META["REMOTE_ADDR"])
    except UserAlreadyVotedError:
        user_already_voted = True

    # logger.debug("info account(" + str(user_id) + "): " + str(account_info))

    context = {
        "user" : account_info,
        "user_contest_info" : contest_account_info,
        "user_already_voted" : user_already_voted,
        "top_five_account" : top_five_account
    }

    return render(request, 'website/catwalk/catwalk_profile.html', context)

def catwalk_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HelpRequestForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():

            messages.add_message(request, messages.SUCCESS, 'La richiesta di aiuto è stata inviata, ti risponderemo appena poss...tut-tut-tut-tut')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/richiesta-aiuto/')

    # if a GET (or any other method) we'll create a blank form
    else:
	# pre-prepopulate post dictionary with current user data
	account_obj =  Account()
        request.POST = account_obj.get_autenticated_user_data(request=request)
        form = HelpRequestForm()

    context = {
        "post" : request.POST,
        "form": form,
    }
    return render(request, 'website/catwalk/catwalk_help.html', context)

def catwalk_report_user(request):
    return render(request, 'website/catwalk/catwalk_report_user.html', False)
# }}}

# private profile {{{
@login_required
def profile_index(request):
    profile_image_form = profileImageForm()
    book_images_form = bookImagesForm()

    # setting a custom cropped images directory
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    request.session['CUSTOM_CROPPED_IMG_DIRECTORY'] = autenticated_user_data["user_id"]

    # TODO: - prelevare l'url dell'immagine profilo
    #       - prelevare x immagini del book e visualizzare il pulsante "mostra
    #         altre" al fondo
    
    profile_url = "upload_image_box/cropped_upload/2/64d88cb7-2f72-40e8-9745-9be8f9303cff.jpg"
    context = {
        "post" : request.POST,
        "profile_image_form": profile_image_form,
        "book_images_form": book_images_form,
        "profile_url": profile_url,
    }

    return render(request, 'website/profile/profile_index.html', context)

@login_required
def profile_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AccountEditForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
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
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():

            messages.add_message(request, messages.SUCCESS, 'Tutte le informazioni sono state salvate correttamente')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/zona-proibita/')

    # if a GET (or any other method) we'll create a blank form
    else:
	# pre-prepopulate post dictionary with current user data
	account_obj =  Account()
        request.POST = account_obj.get_autenticated_user_data(request=request)
        form = Area51Form()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/profile/profile_area51.html', context)
# }}}
