# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from account_app.models.accounts import *
from contest_app.models.contests import *
from contest_app.models.contest_types import *
from contest_app.models.votes import Vote
from beauty_and_pics.common_utils import CommonUtils
from email_template.email.email_template import *
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

def check_if_is_a_catwalker_user(user):
    """ Function to check if user is a catwalker user """
    account_obj =  Account()
    is_catwalker_user = account_obj.check_if_logged_user_is_valid(request_user=user)
    logger.debug("logged user is a catwalker user: " + str(is_catwalker_user))
    return is_catwalker_user

# www {{{
def www_index(request):
    return render(request, 'website/www/www_index.html', False)

def www_how_it_works(request):
    return render(request, 'website/www/www_come_funziona.html', False)

def www_privacy(request):
    return render(request, 'website/www/www_privacy.html', False)

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
            return HttpResponseRedirect('/profilo/1')

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
    # common method class init
    CommonUtils_obj = CommonUtils()

    # retrieve user info
    account_obj =  Account()
    try:
        account_info = account_obj.custom_user_id_data(user_id=user_id)
    except User.DoesNotExist:
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
        vote_obj.check_if_user_can_vote(user_id=user_id, ip_address=CommonUtils_obj.get_ip_address(request=request), request=request)
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
    report_user_obj = account_obj.get_user_about_id(user_id=user_id)

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

    report_user_name = report_user_obj.first_name
    if report_user_obj.last_name:
        report_user_name += " " + report_user_obj.last_name

    context = {
        "report_user_id" : user_id,
        "user_email" : user_email.get("email"),
        "report_user_name" : report_user_name,
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/catwalk/catwalk_report_user.html', context)

@login_required
def profile_unsubscribe(request):

    account_obj = Account()
    user_obj = account_obj.get_user_about_id(user_id=request.user.id)

    # check which notify are enabled
    enable_receive_weekly_report = account_obj.check_bitmask(b1=user_obj.account.newsletters_bitmask, b2=project_constants.WEEKLY_REPORT_EMAIL_BITMASK)
    enable_receive_contest_report = account_obj.check_bitmask(b1=user_obj.account.newsletters_bitmask, b2=project_constants.CONTEST_REPORT_EMAIL_BITMASK)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UnsubscribeForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():
            messages.add_message(request, messages.SUCCESS, 'Le preferenze sono state salvate con successo.')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/disiscriviti/')

    # if a GET (or any other method) we'll create a blank form
    else:
        # pre-prepopulate post dictionary with current user data
        form = UnsubscribeForm()

    context = {
        "post" : request.POST,
        "form": form,
        "enable_receive_weekly_report": enable_receive_weekly_report,
        "enable_receive_contest_report": enable_receive_contest_report,
    }

    return render(request, 'website/profile/profile_unsubscribe.html', context)
# }}}

# private profile {{{
@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_index(request, welcome):
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
        "user_id": autenticated_user_data.get("user_id"),
        "user_first_name": autenticated_user_data.get("first_name"),
        "welcome": welcome,
    }

    return render(request, 'website/profile/profile_index.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
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
@user_passes_test(check_if_is_a_catwalker_user)
def profile_favorites(request):
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    return render(request, 'website/profile/profile_favorites.html', False)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_stats(request):
    # retrieve info about current logged in user
    account_obj = Account()
    account_info = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    # retrieve contest user info
    contest_account_info = account_obj.get_contest_account_info(user_id=account_info["user_id"], contest_type=contest_obj.get_contest_type_from_session(request=request))

    # retrieve favorites count
    favorites_obj = Favorite()
    favorites_count = favorites_obj.count_favorites_about_user_id(user_id=account_info["user_id"])

    context = {
        "user_info" : account_info,
        "user_contest_info" : contest_account_info,
        "favorites_count" : favorites_count,
    }

    return render(request, 'website/profile/profile_stats.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
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

# test email {{{
def email_test(request, email_name, email_mode):
    """View to test email template object"""

    if email_name and email_mode:
        # build email context with all vars
        email_context = {
            "first_name": "Nome",
            "last_name": "Cognome",
            "contest_type": "man_contest",
            "email": "mail@mail.com",
            "password": "pass123",
            "user_email": "user_mail@mail.com",
            "user_id": "2",
            "points": "12345",
            "ranking": "13",
            "help_text": "Ciao ho bisogno di qualche aiuto per...",
            "report_text": "Voglio segnalare l'utente per...",
            "report_user_id": "2",
            "report_user_email": "mailincriminata@mail.com",
            "report_user_profile_url": "http://www.google.com",
        }
        # build requested email template
        email_obj = CustomEmailTemplate(email_name=email_name, email_context=email_context, template_type="user", debug_only=True)

        if email_obj.email_ready_to_send:
            if email_mode == "html":
                email_content = email_obj.get_html_template()
                email_subject = email_obj.email_subject
            elif email_mode == "plain":
                email_content = email_obj.get_plain_template()
                email_subject = email_obj.email_subject
            else:
                email_content = "Please enter a valid visual mode!"
        else:
            email_content = "Please enter a valid template name!"
    else:
        email_content = "Please enter a valid template name and visual mode!"

    return HttpResponse(email_content)
# }}}
