# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from account_app.models.accounts import *
from account_app.models.favorites import *
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
from notify_system_app.models import Notify
from image_contest_app.settings import ICA_LIKE_LIMIT
from image_contest_app.exceptions import ImageAlreadyVotedError, ImageContestClosedError
from image_contest_app.models import ImageContest, ImageContestImage, ImageContestVote
import logging, time

# Get an instance of a logger
logger = logging.getLogger(__name__)

# view decorators {{{
def check_if_is_a_catwalker_user(user):
    """ Function to detect if user is a catwalker user """
    account_obj =  Account()
    is_catwalker_user = account_obj.check_if_logged_user_is_valid(request_user=user)
    if is_catwalker_user:
        logger.debug("logged user IS a catwalker user, email: " + str(user.email) + " (id: " + str(user.id) + ")")

    return is_catwalker_user

def check_if_is_staff_user(user):
    """ Function to detect if user is a staff user """
    account_obj =  Account()
    is_staff_user = account_obj.check_if_logged_user_is_staff(request_user=user)
    if is_staff_user:
        logger.debug("staff user onboard, email: " + str(user.email) + " (id: " + str(user.id) + ")")

    return is_staff_user
# view decorators }}}

# www {{{
def www_index(request):
    return render(request, 'website/www/www_index.html', False)

def www_how_it_works_info(request):
    return render(request, 'website/www/www_how_it_works_info.html', False)

def www_signup_info(request):
    return render(request, 'website/www/www_signup_info.html', False)

def www_contest_info(request):
    return render(request, 'website/www/www_contest_info.html', False)

def www_privacy(request):
    return render(request, 'website/www/www_privacy.html', False)

def www_cookie_policy(request):
    return render(request, 'website/www/www_cookie_policy.html', False)

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
    # if user already registered, redirect to profile page
    if request.user.is_authenticated():
	return HttpResponseRedirect('/profilo/')

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
    account_obj =  Account()

    try:
        # retrieve user info
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
        "absolute_uri" : request.build_absolute_uri(),
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

@ensure_csrf_cookie
def catwalk_photoboard(request, user_id):
    CommonUtils_obj = CommonUtils()
    Contest_obj = Contest()
    ImageContestImage_obj = ImageContestImage()
    ImageContestVote_obj = ImageContestVote()
    account_obj =  Account()
    account_info = {}
    user_can_vote = True

    try:
        # retrieve user contest_type to set contest type in session
        account_info = account_obj.custom_user_id_data(user_id=user_id)
    except User.DoesNotExist:
        # user_id doesn't exists, do nothing
        pass

    # common function to set contest type
    Contest_obj.common_view_set_contest_type(request=request, contest_type=account_info.get("contest_type"))

    # retrieve current contest_type
    contest_type = Contest_obj.get_contest_type_from_session(request=request)

    try:
        # retrieve photoboard user image
        user_contest_image_info = ImageContestImage_obj.get_user_contest_image_info(user_id=user_id)
    except ImageContestImage.DoesNotExist:
        # show photoboard list about this contest_type
	# TODO: se il contest relativo all'utente è chiuso ma l'utente esiste: vvvvvv
	# redirect in pagina profilo utente aprendo popup di errore (foto non più presente per )
        context = {}
        render_page = 'website/catwalk/catwalk_photoboard_list.html'
    else:
        # show only user photoboard image
        try:
            ImageContestVote_obj.image_can_be_voted(image_contest_image_obj=user_contest_image_info.get("user_image_contest_obj"), ip_address=CommonUtils_obj.get_ip_address(request=request), request=request)
        except ImageContestClosedError:
            # TODO ops...contest closed redirect to user profile with alert popoup
            pass
        except ImageAlreadyVotedError:
            # user cannot add like again
            user_can_vote = False
            pass

        context = {
                "user_info" : account_info,
                "user_can_vote" : user_can_vote, # check if this photo can be voted
                "user_image_contest_id" : user_contest_image_info.get("user_image_contest_id"),
                "user_image_contest_url" : user_contest_image_info.get("user_image_contest_url"),
                "user_image_contest_visits": user_contest_image_info.get("user_image_contest_visits"),
                "user_image_contest_like" : user_contest_image_info.get("user_image_contest_like"),
                "user_image_contest_like_remaining": user_contest_image_info.get("user_image_contest_like_remaining"),
                "like_limit" : user_contest_image_info.get("like_limit"),
        }
        render_page = 'website/catwalk/catwalk_photoboard_details.html'

    return render(request, render_page, context)
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

    # current timestamp
    current_timestamp = int(time.time())

    context = {
        "post" : request.POST,
        "profile_image_form": profile_image_form,
        "book_images_form": book_images_form,
        "profile_image_url": profile_image_url,
        "user_id": autenticated_user_data.get("user_id"),
        "user_first_name": autenticated_user_data.get("first_name"),
        "welcome": welcome,
        "current_timestamp": current_timestamp,
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
            messages.add_message(request, messages.SUCCESS, 'Tutte le informazioni sono state salvate correttamente.')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/dati-personali/')

    # if a GET (or any other method) we'll create a blank form
    else:
        # pre-prepopulate post dictionary with current user data
        request.POST = autenticated_user_data
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

    # check if exists favorites about this account
    favorite_obj = Favorite()
    favorite_exists = favorite_obj.count_favorites_about_user_id(user_id=autenticated_user_data["user_id"])

    context = {
        "favorite_exists" : favorite_exists,
    }

    return render(request, 'website/profile/profile_favorites.html', context)

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
            messages.add_message(request, messages.SUCCESS, 'Tutte le informazioni sono state salvate correttamente.')
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
        request.POST = autenticated_user_data
        form = Area51Form()
        delete_user_form = DeleteUserForm()

    context = {
        "post" : request.POST,
        "form": form,
        "delete_user_form": delete_user_form,
    }

    return render(request, 'website/profile/profile_area51.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_notify(request):
    """View to show notify list"""
    # retrieve info about current logged in user
    account_obj = Account()
    account_info = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    # check if exist valid notify
    notify_obj = Notify()
    exist_valid_notify = notify_obj.exist_valid_notify(user_id=request.user.id)

    context = {
            'exist_valid_notify' : exist_valid_notify,
    }

    return render(request, 'website/profile/profile_notify.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_notify_details(request, notify_id):
    """View to show a single notify details"""
    notify_obj = Notify()
    # retrieve info about current logged in user
    account_obj = Account()
    account_info = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    # retrieve user instance
    user_instance = account_obj.get_user_about_id(user_id=request.user.id)
    # retrieve notify instance
    notify_instance = notify_obj.get_notify_instance(notify_id=notify_id, user_id=request.user.id)
    if not notify_instance:
	# notify doesn't exists or belong to another user
	return HttpResponseRedirect('/profilo/notifiche/')
    # retrieve notify details
    notify_details = notify_obj.get_notify_info(notify_instance=notify_instance)
    # mark notify as read
    notify_obj.mark_notify_as_read(notify_instance=notify_instance, user_instance=user_instance)

    context = {
            'notify_creation_date' : notify_details['creation_date'],
            'notify_title' : notify_details['title'],
            'notify_message' : notify_details['message'],
            'notify_action_title' : notify_details['action_title'],
            'notify_action_url' : notify_details['action_url'],
    }

    return render(request, 'website/profile/profile_notify_details.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_control_panel(request):
    """View to show control panel page"""
    # retrieve info about current logged in user
    account_obj = Account()
    account_info = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    return render(request, 'website/profile/profile_control_panel.html', False)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_advise(request):
    """View to show advise page"""
    # retrieve info about current logged in user
    account_obj = Account()
    account_info = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

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
            messages.add_message(request, messages.SUCCESS, 'Tutte le informazioni sono state salvate correttamente.')
            # redirect to user profile
            return HttpResponseRedirect('/profilo/avvisi/')

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

    return render(request, 'website/profile/profile_advise.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_gain_points(request):
    """View to show gain more points page"""
    # retrieve info about current logged in user
    account_obj = Account()
    account_info = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    profile_page_url = settings.SITE_URL + "/passerella/dettaglio-utente/" + str(request.user.id)

    context = {
        "profile_page_url" : profile_page_url,
        "share_text" : "Votatemi su: ",
    }

    return render(request, 'website/profile/profile_gain_points.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_photoboard(request, add_success):
    """View to show photo board page"""

    user_obj = request.user
    user_id = user_obj.id

    # retrieve info about current logged in user
    account_obj = Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    # check if already exists an image for this user in photoboard
    ImageContestImage_obj = ImageContestImage()
    if ImageContestImage_obj.image_exists(user_id=user_id):
        # l'utente ha già selezionato una foto per la bacheca, prelevo l'url dell'immagine
        user_contest_image_info = ImageContestImage_obj.get_user_contest_image_info(user_id=user_id)

        context = {
            "user_id": user_id,
            "user_image_contest_info": user_contest_image_info,
            "add_success": add_success,
        }
        render_page = 'website/profile/profile_photoboard_details.html'
    else:
        # l'utente non ha ancora selezionato una foto per la bacheca
        context = {
            "user_id": user_id,
        }
        render_page = 'website/profile/profile_photoboard_list.html'

    return render(request, render_page, context)
# }}}

# test email {{{
@login_required
@user_passes_test(check_if_is_staff_user)
def email_test(request, email_name, email_mode):
    """View to test email template object"""

    if email_name and email_mode:
        # build email context with all vars
        email_context = {
            "first_name": "Nome",
            "last_name": "Cognome",
            "contest_type": "man-contest",
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
# custom error pages {{{
def custom404_view(request):
    """Custom 404 page"""
    response = render_to_response('website/www/www_404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404

    return response

def custom500_view(request):
    """Custom 500 page"""
    response = render_to_response('website/www/www_500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500

    return response
# custom error pages }}}

# landing pages {{{
def landing_landing1(request):
    """Landing page 1 - concorso per modelle"""
    return render(request, 'website/landing/landing1.html', False)
def landing_landing2(request):
    """Landing page 2 - tendenze moda"""
    return render(request, 'website/landing/landing2.html', False)
# landing pages }}}
