# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from account_app.models.accounts import *
from account_app.models.images import Book
from account_app.models.favorites import *
from contest_app.models.contests import *
from contest_app.models.contest_types import *
from contest_app.models.votes import Vote
from contest_app.models.hall_of_fame import HallOfFame
from django_survey.models import UserAnswer, UserSurvey
from django_survey.settings import DS_CONST_NOT_PUBLISHED, DS_CONST_PUBLISHED, DS_CONST_PENDING_APPROVAL, DS_CONST_APPROVED, DS_CONST_NOT_APPROVED
from beauty_and_pics.common_utils import CommonUtils
from email_template.email.email_template import *
# loading forms
from custom_form_app.forms.register_form import *
from custom_form_app.forms.fast_register_form import *
from custom_form_app.forms.login_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from custom_form_app.forms.delete_user_form import *
from custom_form_app.forms.help_request_form import *
from custom_form_app.forms.report_user_form import *
from custom_form_app.forms.upload_book_form import *
from custom_form_app.forms.unsubscribe_form import *
from custom_form_app.forms.get_prize_form import GetPrizeForm
from custom_form_app.forms.survey_form import SurveyForm
from notify_system_app.models import Notify
from image_contest_app.settings import ICA_LIKE_LIMIT
from website.exceptions import ContestClosedNotExistsError
from image_contest_app.exceptions import ImageAlreadyVotedError, ImageContestClosedError
from image_contest_app.models import ImageContest, ImageContestImage, ImageContestVote
# from django_survey.models import Answer
import logging, time, urllib

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
def www_email_confirm(request, auth_token):
    """View to confirm email address"""

    # check if there is Account which matches the activation key (if not then display 404)
    account_obj = get_object_or_404(Account, activation_key=auth_token)

    # check if user email was already confirmed
    if account_obj.has_permission(user_obj=account_obj.user, permission_codename='user_verified'):
        return HttpResponseRedirect('/profilo/')

    # send welcome email
    email_context = { "first_name": account_obj.user.first_name }
    CustomEmailTemplate(email_name="welcome_email", email_context=email_context, template_type="user", recipient_list=[account_obj.user.email,])

    # setting user as verified
    account_obj.add_user_permission(user_obj=account_obj.user, permission_codename='user_verified')

    return HttpResponseRedirect('/email-confermata/')

def www_email_successfully_confirmed(request):
    """View shown after email confirmation"""
    return render(request, 'website/www/www_email_successfully_confirmed.html', False)

def www_index(request):
    """View to show home page, and contest_type winners if exist"""
    HallOfFame_obj = HallOfFame()

    # retrieve contest_type codes
    woman_contest_code = project_constants.WOMAN_CONTEST
    man_contest_code = project_constants.MAN_CONTEST

    # retrieve contest winners (if exists)
    woman_contest_winner = HallOfFame_obj.get_user_for_winner_block(contest_type=woman_contest_code)
    man_contest_winner = HallOfFame_obj.get_user_for_winner_block(contest_type=man_contest_code)

    """
    try:
        # se esiste un vincitore per l'ultimo contest chiuso, lo mostro in home page
        woman_contest_winner = {}
        woman_contest_winner = HallOfFame_obj.get_hall_of_fame_user(contest_type=project_constants.WOMAN_CONTEST)
    except ContestClosedNotExistsError, ContestTypeRequiredError:
        # il contest_type non ha contest chiusi, mostro immagine di default
        pass

    try:
        # se esiste un vincitore per l'ultimo contest chiuso, lo mostro in home page
        man_contest_winner = {}
        man_contest_winner = HallOfFame_obj.get_hall_of_fame_user(contest_type=project_constants.MAN_CONTEST)
    except ContestClosedNotExistsError, ContestTypeRequiredError:
        # il contest_type non ha contest chiusi, mostro immagine di default
        pass
    """

    context = {
        "woman_contest_code" : woman_contest_code,
        "man_contest_code" : man_contest_code,
        "woman_contest_winner" : woman_contest_winner,
        "man_contest_winner" : man_contest_winner,
    }

    return render(request, 'website/www/www_index.html', context)

def www_how_it_works_info(request):
    return render(request, 'website/www/www_how_it_works_info.html', False)

def www_signup_info(request):
    return render(request, 'website/www/www_signup_info.html', False)

def www_contest_info(request):
    return render(request, 'website/www/www_contest_info.html', False)

def www_privacy(request):
    return render(request, 'website/www/www_privacy.html', False)

def www_terms(request):
    return render(request, 'website/www/www_terms.html', False)

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
    return HttpResponseRedirect('/')
    # return render(request, 'website/www/www_index.html', False)

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
    """View to show register page"""

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
            # altrimenti redirect to user profile
            return HttpResponseRedirect('/profilo/1')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/www/www_register.html', context)

def www_fast_register(request, user_id):
    """
        View to show a fast register page, will be requested only:
        first_name, gender, email, password
    """

    # if user already registered, redirect to profile page
    if request.user.is_authenticated():
	return HttpResponseRedirect('/profilo/')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FastRegisterForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():
            if user_id:
                # se settato uno user id faccio redirect verso l'utente, mostrando un messaggio di successo
                messages.add_message(request, settings.POPUP_SIMPLE_MESSAGE, 'Grazie per la registrazione, ora puoi proseguire con le votazioni.')
                return HttpResponseRedirect('/passerella/dettaglio-utente/' + str(user_id))
            else:
                # altrimenti redirect to user profile
                return HttpResponseRedirect('/passerella/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FastRegisterForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'website/www/www_fast_register.html', context)

def www_ranking_contest(request, contest_type, contest_year):
    """view to show a ranking table about contest and year"""
    # se l'anno non è specificato mi baso sull'ultimo contest chiuso
    Contest_Type_obj = Contest_Type()
    HallOfFame_obj = HallOfFame()

    # check if contest_type exists, otherwise raise a 404
    current_contest_type_obj = Contest_Type_obj.get_contest_type_by_code(code=contest_type)
    if not current_contest_type_obj:
        raise Http404()

    # retrieve top 100 users
    # potrebbe essere una lista vuota in due casi, o la data selezionata non contiene nessun contest,
    # oppure il contest esiste ma non è presente nessun partecipante con almeno un voto (quasi impossibile)
    top_100_users = None
    try:
        top_100_users = HallOfFame_obj.get_hall_of_fame_elements(contest_type=contest_type, contest_year=contest_year)
    except ContestClosedNotExistsError:
        # non esistono ancora concorsi chiusi
        pass

    # retrieve contest year (ho fatto così perchè se contest_year non venisse passato ci si riferirebbe
    # all'ultimo concorso chiuso prima di questo attivo, in questa maniera riesco a prelevare la data corretta
    contest_start_date = None
    if top_100_users:
	contest_start_date = top_100_users[0]["contest__start_date"]

    # retrieve contest name
    contest_name = current_contest_type_obj.description

    context = {
        "top_100_users": top_100_users,
        "contest_name": contest_name,
        "contest_start_date": contest_start_date, # cambiare il nome in "contest_start_date"
        "contest_type": contest_type,
    }

    return render(request, 'website/www/www_ranking_contest.html', context)

def www_podium(request, contest_type, contest_year, user_id):
    """view to to show podium user about contest_type, contest_year and user_id"""
    # se l'anno non è specificato mi baso sull'ultimo contest chiuso
    Contest_Type_obj = Contest_Type()
    HallOfFame_obj = HallOfFame()
    hall_of_fame_user = None

    # check if contest_type exists, otherwise raise a 404
    current_contest_type_obj = Contest_Type_obj.get_contest_type_by_code(code=contest_type)
    if not current_contest_type_obj:
        raise Http404()

    if user_id:
        # retrieve podium user
        # prelevo un utente specifico tra i top 100
        try:
            hall_of_fame_user = HallOfFame_obj.get_hall_of_fame_user(contest_type=contest_type, contest_year=contest_year, user_id=user_id)
        except ContestClosedNotExistsError, ContestTypeRequiredError:
            # non esistono ancora concorsi chiusi o nessun contest type passato
            raise Http404()

    # check if user is a podium user (posizione compresa tra 1 e 5)
    is_valid_podium_user = HallOfFame_obj.is_a_podium_user(hall_of_fame_user_row=hall_of_fame_user)
    if not hall_of_fame_user or not is_valid_podium_user:
        # utente non esistente o non sul podio, l'utente non sarebbe dovuto arrivare in questa pagina
        raise Http404()

    # retrieve contest year (ho fatto così perchè se contest_year non venisse passato ci si riferirebbe
    # all'ultimo concorso chiuso prima di questo attivo, in questa maniera riesco a prelevare la data corretta
    contest_start_date = None
    if hall_of_fame_user:
	contest_start_date = hall_of_fame_user["contest__start_date"]

    # retrieve contest name
    contest_name = current_contest_type_obj.description

    context = {
        "podium_user": hall_of_fame_user,
        "contest_name": contest_name,
        "contest_start_date": contest_start_date,
        "podium_string": HallOfFame_obj.get_podium_page_string(contest_type=contest_type, ranking=hall_of_fame_user.get("ranking")),
	"contest_type": contest_type,
    }

    return render(request, 'website/www/www_podium.html', context)

def www_howto_votations(request):
    """view to show howto about votations"""
    return render(request, 'website/www/howto/www_howto_votations.html', False)

def www_features(request):
    """view to show platform features"""
    return render(request, 'website/www/www_features.html', False)

def www_faq(request):
    """view to show FAQ page"""
    return render(request, 'website/www/www_faq.html', False)
# }}}

# catwalk {{{
@ensure_csrf_cookie
def catwalk_index(request, contest_type=None):
    # set current contest_type
    contest_winner = None
    HallOfFame_obj = HallOfFame()
    Contest_obj = Contest()

    # common function to set contest type
    Contest_obj.common_view_set_contest_type(request=request, contest_type=contest_type)

    # retrieve contest_type
    contest_type = Contest_obj.get_contest_type_from_session(request=request)

    # retrieve contest winner for catwalk index
    contest_winner = HallOfFame_obj.get_user_for_winner_block(contest_type=contest_type)

    context = {
	"contest_winner": contest_winner,
    }

    return render(request, 'website/catwalk/catwalk_index.html', context)

@ensure_csrf_cookie
def catwalk_profile(request, user_id):
    # common method class init
    CommonUtils_obj = CommonUtils()
    account_obj = Account()
    vote_obj = Vote()
    book_obj = Book()
    contest_obj = Contest()
    favorite_obj = Favorite()
    user_answer_obj = UserAnswer()

    try:
        # retrieve user info
        account_info = account_obj.custom_user_id_data(user_id=user_id)
    except User.DoesNotExist:
        # user id doesn't exists
        return HttpResponseRedirect('/index/')

    # set current contest_type
    contest_obj.set_contest_type(request=request, contest_type=account_info["contest_type"])

    # retrieve contest user info
    contest_account_info = account_obj.get_contest_account_info(user_id=user_id, contest_type=contest_obj.get_contest_type_from_session(request=request))

    # retrieve profile image url
    profile_image_url = book_obj.get_profile_image_url(user_id=user_id)

    # get user survey questions and answers (per mostrare l'intervista)
    interview_questions_answers = user_answer_obj.get_survey_answers_by_user_id(survey_code='interview', user_id=user_id, gender=account_info.get("gender"), only_if_published=True)

    contest_is_open = False
    user_already_registered = False
    email_is_verified = False
    user_already_voted = False

    # check if favorite already exists for this account 
    user_already_favorite = favorite_obj.check_if_favorite_exists(user_id=request.user.id, favorite_user_id=user_id)

    # controlli annidati
    # 1 contest is open? -- nel popup
    # 3 userRegistered? -- nel popup
    # 4 emailVerified? -- nel popup
    # 2 user already voted? -- fuori dal popup

    # 1) controllo che il contest sia aperto
    if contest_obj.check_if_account_contest_is_active(user_id=user_id):
        contest_is_open = True
        # 2) controllo che l'utente sia registrato
        if request.user.id:
            user_already_registered = True
            # 3) controllo che la mail dell'utente sia verificata
            if account_obj.has_permission(user_obj=request.user, permission_codename='user_verified'):
                email_is_verified = True
                # 4) controllo che l'utente non abbia già votato
                try:
                    vote_obj.check_if_user_can_vote(from_user_id=request.user.id, to_user_id=user_id, request=request)
                except UserAlreadyVotedError:
                    # user already voted
                    user_already_voted = True

    context = {
        "user_info" : account_info,
        "user_contest_info" : contest_account_info,
        "profile_image_url" : profile_image_url,
        "user_already_favorite" : user_already_favorite,
        "user_is_authenticated" : request.user.is_authenticated,
        "absolute_uri" : request.build_absolute_uri(),
        "contest_is_open" : contest_is_open,
        "user_already_registered" : user_already_registered,
        "email_is_verified" : email_is_verified,
        "user_already_voted" : user_already_voted,
        "interview_questions_answers" : interview_questions_answers,
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
            messages.add_message(request, messages.SUCCESS, 'L\'utente è stato segnalato, stiamo verificando!')
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
def catwalk_photoboard_list(request):
    # view to show photoboard list about this contest_type
    CommonUtils_obj = CommonUtils()
    Contest_obj = Contest()
    ImageContestImage_obj = ImageContestImage()

    # common function to set contest type
    Contest_obj.common_view_set_contest_type(request=request)

    # retrieve current contest_type
    contest_type = Contest_obj.get_contest_type_from_session(request=request)

    # check if exist images in current active contest
    images_exist = ImageContestImage_obj.images_exist_in_active_contest(contest_type=contest_type)

    context = {
        "images_exist": images_exist,
    }

    return render(request, 'website/catwalk/catwalk_photoboard_list.html', context)

@ensure_csrf_cookie
def catwalk_photoboard_details(request, user_id):
    # view to show only user photoboard image
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

    # user_id doesn't exist, redirect to catwalk page
    if not account_obj.check_if_user_id_exists(user_id=user_id):
        return HttpResponseRedirect('/passerella/')

    try:
        # retrieve photoboard user image
        user_contest_image_info = ImageContestImage_obj.get_user_contest_image_info(user_id=user_id)
    except ImageContestImage.DoesNotExist:
        # non esiste la foto bacheca dell'utente passato
        # - redirect in pagina profilo utente aprendo popup di errore "Ci spiace, la foto non più presente per la votazione":
	messages.add_message(request, settings.POPUP_ALERT, 'Ci spiace, la foto non è più presente per la votazione.')
        return HttpResponseRedirect('/passerella/dettaglio-utente/' + str(user_id))

    try:
        ImageContestVote_obj.image_can_be_voted(image_contest_image_obj=user_contest_image_info.get("user_image_contest_obj"), ip_address=CommonUtils_obj.get_ip_address(request=request), request=request)
    except ImageContestClosedError:
        # se contest foto bacheca è chiuso
        # - redirect in pagina profilo utente aprendo popup di errore "Ci spiace, la foto non più presente per la votazione":
	messages.add_message(request, settings.POPUP_ALERT, 'Ci spiace, la foto non è più presente per la votazione.')
        return HttpResponseRedirect('/passerella/dettaglio-utente/' + str(user_id))
    except ImageAlreadyVotedError:
        # user cannot add like again
        user_can_vote = False
        pass

    # add a visit to this image
    ImageContestImage_obj.add_image_visit(image_contest_image_id=user_contest_image_info.get("user_image_contest_id"))

    context = {
            "user_info" : account_info,
            "user_can_vote" : user_can_vote, # check if this photo can be voted
            "user_image_contest_id" : user_contest_image_info.get("user_image_contest_id"),
            "user_image_contest_url" : user_contest_image_info.get("user_image_contest_url"),
            "user_image_contest_visits": user_contest_image_info.get("user_image_contest_visits"),
            "user_image_contest_like" : user_contest_image_info.get("user_image_contest_like"),
            "user_image_contest_like_remaining": user_contest_image_info.get("user_image_contest_like_remaining"),
            "like_limit" : user_contest_image_info.get("like_limit"),
            "absolute_uri" : request.build_absolute_uri(),
    }

    return render(request, 'website/catwalk/catwalk_photoboard_details.html', context)
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

    # se l'utente non è abilitato per richiedere il premio, nascondo il box
    user_can_show_get_prize_button = False
    prize_can_be_redeemed = account_obj.get_if_prize_can_be_redeemed(prize_status=account_info["prize_status"])
    prize_was_already_redeemed = account_obj.get_if_prize_was_already_redeemed(prize_status=account_info["prize_status"])
    if prize_can_be_redeemed or prize_was_already_redeemed:
        user_can_show_get_prize_button = True

    context = {
        "user_can_show_get_prize_button": user_can_show_get_prize_button,
    }

    return render(request, 'website/profile/profile_control_panel.html', context)

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
def profile_photoboard(request, image_add_success):
    """View to show photoboard page"""

    user_obj = request.user
    user_id = user_obj.id
    Contest_obj = Contest()
    account_obj = Account()
    Book_obj = Book()

    # retrieve info about current logged in user
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)

    # set current contest_type
    Contest_obj.common_view_set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    # check if already exists an image for this user in photoboard
    ImageContestImage_obj = ImageContestImage()
    if ImageContestImage_obj.image_exists_in_active_contest(user_id=user_id):
        # l'utente ha già inserito una foto nella bacheca
        # quindi prelevo l'url dell'immagine e altre info
        user_contest_image_info = ImageContestImage_obj.get_user_contest_image_info(user_id=user_id)
	# photoboard image url
	photoboard_image_url = settings.SITE_URL + "/passerella/bacheca/" + str(user_id) + "/"

	# se l'utente ha appena inserito l'immagine nella bacheca mostro un popup di successo
	if image_add_success:
	    messages.add_message(request, settings.POPUP_SIMPLE_MESSAGE, 'Immagine inserita correttamente nella bacheca. Condividi la foto il più possibile per guadagnare <b>' + str(ICA_LIKE_LIMIT) + ' mi piace</b> ed ottenere il posto nella passerella!')

        context = {
            "user_id": user_id,
            "user_image_contest_info": user_contest_image_info,
            "photoboard_image_url": photoboard_image_url,
        }
        render_page = 'website/profile/profile_photoboard_details.html'
    else:
        # l'utente non ha ancora inserito una foto nella bacheca, oppure è
        # presente un vincitore e il photoboard è stato chiuso
        photoboard_contest_winner = ImageContestImage_obj.get_closed_contest_info(contest_type=autenticated_user_data["contest_type"])

        # è già presente un vincitore per il contest, non è possibile aggiungere adesso una foto in bacheca
        enable_image_selection = True
        if photoboard_contest_winner:
            enable_image_selection = False

        # check if current user win the photoboard contest
        user_is_winner = False
        if photoboard_contest_winner.get("user__id") == user_id:
            user_is_winner = True

        # tra quanti gg è possibile nuovamente aggiungere immagini nella bacheca
        next_selection_date = 0
        if photoboard_contest_winner.get("image_contest__expiring"):
            next_selection_date = photoboard_contest_winner.get("image_contest__expiring")

	# check if exists book images
	exists_user_images = Book_obj.exists_user_images(user_id=user_id)

        context = {
            "user_id": user_id,
            "user_is_winner": user_is_winner,
            "enable_image_selection": enable_image_selection,
            "next_selection_date": next_selection_date,
            "exists_user_images": exists_user_images,
            "contest_like_limit": ICA_LIKE_LIMIT,
        }
        render_page = 'website/profile/profile_photoboard_list.html'

    return render(request, render_page, context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_get_prize(request):
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    # check if user can redeem prize
    if not account_obj.get_if_prize_can_be_redeemed(prize_status=autenticated_user_data["prize_status"]):
        # redirect to control panel page
        return HttpResponseRedirect('/profilo/pannello-di-controllo/')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GetPrizeForm(request.POST)
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():
            # redirect to get_prize page
            return HttpResponseRedirect('/profilo/ottieni-premio/')

    # if a GET (or any other method) we'll create a blank form
    else:
        # pre-prepopulate post dictionary with current user data
        request.POST = autenticated_user_data
        form = GetPrizeForm()

    # check if prize was already redeemed
    prize_was_already_redeemed = account_obj.get_if_prize_was_already_redeemed(prize_status=autenticated_user_data["prize_status"])

    context = {
        "post": request.POST,
        "form": form,
        "prize_was_already_redeemed": prize_was_already_redeemed,
    }

    return render(request, 'website/profile/profile_get_prize.html', context)

#TODO: check dei parametri addizionali passati nei form
@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_interview(request):
    """Create interview view"""
    survey_code = 'interview'
    user_answer_obj = UserAnswer()
    # set current contest_type
    account_obj =  Account()
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    contest_obj = Contest()
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SurveyForm(request.POST, extra_param1=survey_code, extra_param2=autenticated_user_data.get('gender'))
        form.set_current_request(request=request)

        # check whether it's valid:
        if form.is_valid() and form.form_actions():
            # redirect to get_prize page
            return HttpResponseRedirect('/profilo/pubblicazione-intervista/')

    # if a GET (or any other method) we'll create a blank form
    else:
        # pre-prepopulate post dictionary with current user data
        request.POST = user_answer_obj.get_survey_answers_form_by_user_id(survey_code=survey_code, user_id=request.user.id)
	logger.info("saved questions: " + str(request.POST))
        form = SurveyForm(extra_param1=survey_code, extra_param2=autenticated_user_data.get('gender'))

    context = {
	"user_first_name": autenticated_user_data["first_name"],
        "post" : request.POST,
        "form": form,
        "extra_param1": survey_code,
        "extra_param2": autenticated_user_data.get('gender'),
    }

    return render(request, 'website/profile/profile_interview.html', context)

@login_required
@user_passes_test(check_if_is_a_catwalker_user)
def profile_interview_publishing(request):
    """Publish created interview view"""
    user_survey_obj = UserSurvey()
    user_answer_obj = UserAnswer()
    account_obj =  Account()
    contest_obj = Contest()
    survey_code = 'interview'

    # get logged in user data
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    # set current contest_type
    contest_obj.set_contest_type(request=request, contest_type=autenticated_user_data["contest_type"])

    """
    Controllo se esiste un survey per questo id_utente e survey_code = inteview:
    - se esiste lo stampo come anteprima
    - altrimenti redirect nella pagina per crearlo
    """

    try:
        # check if already exists a survey about this user
        existing_user_survey_obj = user_survey_obj.get_user_survey(survey_code=survey_code, user_id=request.user.id)
    except UserSurvey.DoesNotExist:
        # redirect nella pagina per creare l'intervista
        return HttpResponseRedirect('/profilo/intervista/')

    # retrieve survey publishing and approving status
    publishing_status = existing_user_survey_obj.published
    approving_status = existing_user_survey_obj.status

    # retrieve survey publishing status label and approving status label
    publishing_status_label = user_survey_obj.get_survey_publishing_label(publishing_status=publishing_status)
    approving_status_label = user_survey_obj.get_survey_approving_label(approving_status=approving_status)

    # get user survey questions and answers (per mostrare la preview del survey)
    user_questions_answers = user_answer_obj.get_survey_answers_by_user_id(survey_code=survey_code, user_id=request.user.id, gender=autenticated_user_data.get("gender"))

    # se il survey non è stato approvato prelevo l'eventuale check_message
    check_message = False
    if publishing_status == DS_CONST_NOT_APPROVED:
        check_message = existing_user_survey_obj.check_message

    context = {
        "survey_code" : survey_code,
        "check_message" : check_message,
        "survey_questions" : user_questions_answers,
        "publish_status" : publishing_status,
        "approving_status" : approving_status,
        "publish_status_label" : publishing_status_label,
        "approving_status_label" : approving_status_label,
        "published_status" : DS_CONST_PUBLISHED,
        "not_published_status" : DS_CONST_NOT_PUBLISHED,
        "pending_approval_status" : DS_CONST_PENDING_APPROVAL,
        "approved_status" : DS_CONST_APPROVED,
        "not_approved_status" : DS_CONST_NOT_APPROVED,
    }

    return render(request, 'website/profile/profile_interview_publishing.html', context)
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
def beauty_and_pics(request):
    """Landing beauty_and_pics - presentazione del concorso"""
    return render(request, 'website/landing/beauty_and_pics.html', False)
# landing pages }}}
