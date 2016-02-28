# -*- coding: utf-8 -*-

# contest processor to manage common vars
from django.conf import settings
from account_app.models.accounts import *
from account_app.models.images import *
from contest_app.models.contests import *
# from image_contest_app.models import ImageContestImage, ImageContest #imagecontestapptag
from notify_system_app.models import Notify
from django_survey.models import Survey
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def common_contest_processors(request):
    """Common template context processor function"""
    account_obj =  Account()
    book_obj = Book()
    contest_obj = Contest()
    survey_obj = Survey()
    # ImageContest_obj = ImageContest() #imagecontestapptag
    # ImageContestImage_obj = ImageContestImage() #imagecontestapptag
    Notify_obj = Notify()
    contest_type = contest_obj.get_contest_type_from_session(request=request)
    logged_user_id = None
    show_email_confirm_bar = False
    logger.info("@@@current contest_type: " + str(contest_type))

    ### template context vars {{{ ###
    # top five user ranking
    top_five_account = account_obj.get_top_five_contest_user(contest_type=contest_type)
    # profile thumbnail image url
    profile_thumbnail_image_url = None
    # current contest start_time
    contest_info = contest_obj.get_contest_info_about_type(contest_type=contest_type)
    exists_active_photoboard = False
    photoboard_contest_winner = False
    # check if exists an active photoboard
    # exists_active_photoboard = ImageContest_obj.exists_active_contest(contest_type=contest_type) #imagecontestapptag
    # last photoboard contest winner
    # photoboard_contest_winner = ImageContestImage_obj.get_closed_contest_info(contest_type=contest_type) #imagecontestapptag

    # manage survey
    survey_obj._manage_surveys()

    # shown user notify popup
    check_user_notify = False
    ### template context vars }}} ###

    # check if user is authenticated
    user_is_authenticated = account_obj.check_if_logged_user_is_valid(request_user=request.user)
    # retrieve authenticated user data
    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    if autenticated_user_data.get("user_id"):
        # user LOGGED in
        # retrieve logged user profile thumbnail url
        profile_thumbnail_image_url = book_obj.get_profile_thumbnail_image_url(user_id=autenticated_user_data["user_id"])
        # retrieve logged user id
        logged_user_id = autenticated_user_data.get("user_id")
	# count unread notify number TODO: aggiungere icona notifiche nel menu
	# unread_notify_number = Notify_obj.count_notify_to_read(user_id=logged_user_id)

	# check if user notify popup must be shown: if not exists cookie -> show user notify popup
        if not request.COOKIES.get(project_constants.USER_NOTIFY_POPUP_SHOWN_COOKIE_NAME):
            check_user_notify = True

        # check if user email was already confirmed
        if not account_obj.has_permission(user_obj=request.user, permission_codename='user_verified'):
            show_email_confirm_bar = True # flag to show/hide email confirmation bar
    else:
        # user NOT LOGGED in
        pass

    return {
            'top_five_account': top_five_account,
            'profile_thumbnail_image_url': profile_thumbnail_image_url,
            'contest_info': contest_info,
            'photoboard_contest_winner': photoboard_contest_winner,
            'user_is_authenticated': user_is_authenticated,
            'authenticated_user_contest_type': autenticated_user_data.get("contest_type"),
            'site_name': project_constants.SITE_NAME,
            'logged_user_id': logged_user_id,
            'check_user_notify': check_user_notify,
            'message_tags': settings.POPUP_TAGS,
            'exists_active_photoboard': exists_active_photoboard,
            'static_url': settings.STATIC_URL,
            'show_email_confirm_bar': show_email_confirm_bar,
    }
