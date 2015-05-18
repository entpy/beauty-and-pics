# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from account_app.models.accounts import *
from contest_app.models.contests import *
from contest_app.models.contest_types import *
from contest_app.models.votes import Vote
# loading forms
from custom_form_app.forms.register_form import *
from custom_form_app.forms.login_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from custom_form_app.forms.delete_user_form import *
from custom_form_app.forms.help_request_form import *
from custom_form_app.forms.report_user_form import *
from custom_form_app.forms.upload_book_form import *
from custom_form_app.forms.unsubscribe_form import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# www {{{
def www_index(request):
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
            account_obj =  Account()
            autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
	    if request.GET.get('next'):
		# redirect to custom url
		return HttpResponseRedirect(request.GET.get('next'))
	    else:
		# redirect to catwalk
		return HttpResponseRedirect('/passerella/' + str(autenticated_user_data["contest_type"]))

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
def catwalk_index(request, contest_type=None):
    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=contest_type)

    return render(request, 'website/catwalk/catwalk_index.html', False)

@ensure_csrf_cookie
def catwalk_profile(request, user_id):
    # retrieve user info
    account_obj =  Account()
    try:
        account_info = account_obj.custom_user_id_data(user_id=user_id)
    except Account.DoesNotExist:
        # user id doesn't exists
        return HttpResponseRedirect('/index/')

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    # retrieve contest user info
    contest_account_info = account_obj.get_contest_account_info(user_id=user_id, contest_type=contest_obj.get_contest_type_from_session(request=request))

    # retrieve profile image url
    book_obj = Book()
    profile_image_url = book_obj.get_profile_image_url(user_id=user_id)

    # check if this catwalker can be voted
    vote_obj = Vote()
    user_already_voted = False
    try:
        vote_obj.check_if_user_can_vote(user_id=user_id, ip_address=request.META["REMOTE_ADDR"])
    except UserAlreadyVotedError:
        user_already_voted = True

    # check if favorite already exists for this account 
    favorite_obj = Favorite()
    user_already_favorite = favorite_obj.check_if_favorite_exists(user_id=request.user.id, favorite_user_id=user_id)

    # logger.debug("info account(" + str(user_id) + "): " + str(account_info))

    context = {
        "user_info" : account_info,
        "user_contest_info" : contest_account_info,
        "user_already_voted" : user_already_voted,
        "profile_image_url" : profile_image_url,
        "user_already_favorite" : user_already_favorite,
        "user_is_authenticated" : request.user.is_authenticated,
    }

    return render(request, 'website/catwalk/catwalk_profile.html', context)

@ensure_csrf_cookie
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
            return HttpResponseRedirect('/passerella/richiesta-aiuto/')

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

@ensure_csrf_cookie
def catwalk_report_user(request, user_id):

    # retrieve current logged in user email
    account_obj =  Account()
    user_email = account_obj.get_autenticated_user_data(request=request)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportUserForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():
            messages.add_message(request, messages.SUCCESS, 'L\'utente è stato segnalato, prenderemo dei provvedimenti appena possibile')
            # redirect to user profile
            return HttpResponseRedirect('/passerella/segnalazione-utente/' + user_id + '/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReportUserForm()

    context = {
        "report_user_id" : user_id,
        "user_email" : user_email.get("email"),
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/catwalk/catwalk_report_user.html', context)

@ensure_csrf_cookie
def catwalk_unsubscribe(request, user_email):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UnsubscribeForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():
            messages.add_message(request, messages.SUCCESS, 'Ti sei disiscritto dalla reportistica mensile.')
            # redirect to user profile
            return HttpResponseRedirect('/passerella/disiscriviti/')

    # if a GET (or any other method) we'll create a blank form
    else:
        # pre-prepopulate post dictionary with current user data
        form = UnsubscribeForm()

    context = {
        "user_email" : user_email,
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/catwalk/catwalk_unsubscribe.html', context)
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

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    # retrieve profile image url
    book_obj = Book()
    profile_image_url = book_obj.get_profile_image_url(user_id=autenticated_user_data["user_id"])

    context = {
        "post" : request.POST,
        "profile_image_form": profile_image_form,
        "book_images_form": book_images_form,
        "profile_image_url": profile_image_url,
        "user_id": autenticated_user_data["user_id"],
    }

    return render(request, 'website/profile/profile_index.html', context)

@login_required
def profile_data(request):
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

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
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    return render(request, 'website/profile/profile_favorites.html', False)

@login_required
def profile_stats(request):
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    return render(request, 'website/profile/profile_stats.html', False)

@login_required
def profile_area51(request):
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

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

        # delete user block
        delete_user_form = DeleteUserForm(request.POST)
        delete_user_form.set_current_request(request=request)

        # check whether it's valid:
        if delete_user_form.is_valid() and delete_user_form.form_actions():
            # redirect to logout page
            return HttpResponseRedirect('/logout')

    # if a GET (or any other method) we'll create a blank form
    else:
        # pre-prepopulate post dictionary with current user data
        account_obj =  Account()
        request.POST = account_obj.get_autenticated_user_data(request=request)
        form = Area51Form()
        delete_user_form = DeleteUserForm()

    context = {
        "post" : request.POST,
        "form": form,
        "delete_user_form": delete_user_form,
    }

    return render(request, 'website/profile/profile_area51.html', context)
# }}}
