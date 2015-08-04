# contest processor to manage common vars
from account_app.models.accounts import *
from account_app.models.images import *
from contest_app.models.contests import *
from contest_app.models.hall_of_fame import *
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def common_contest_processors(request):
    """Common template context processor function"""
    account_obj =  Account()
    book_obj = Book()
    contest_obj = Contest()
    hall_of_fame_obj = HallOfFame()
    contest_type = contest_obj.get_contest_type_from_session(request=request)
    logged_user_id = None
    logger.info("@@@current contest_type: " + str(contest_type))

    ### template context vars {{{ ###
    # top five user ranking
    top_five_account = account_obj.get_top_five_contest_user(contest_type=contest_type)
    # profile thumbnail image url
    profile_thumbnail_image_url = None
    # current contest start_time
    contest_info = contest_obj.get_contest_info_about_type(contest_type=contest_type)
    # last contest winner
    contest_winner = hall_of_fame_obj.get_last_active_contest_winner(contest_type=contest_type)
    ### template context vars }}} ###

    # check if user is authenticated
    user_is_authenticated = account_obj.check_if_logged_user_is_valid(request_user=request.user)

    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    if autenticated_user_data.get("user_id"):
        # logger.debug("[TEMPLATE_PROCESSOR] user logged in (user id: " + str(autenticated_user_data["user_id"]) + ")")
        profile_thumbnail_image_url = book_obj.get_profile_thumbnail_image_url(user_id=autenticated_user_data["user_id"])
        logged_user_id = autenticated_user_data.get("user_id")
    else:
        # logger.debug("[TEMPLATE_PROCESSOR] user NOT logged in")
        pass

    return {
            'top_five_account': top_five_account,
            'profile_thumbnail_image_url': profile_thumbnail_image_url,
            'contest_info': contest_info,
            'contest_winner': contest_winner,
            'user_is_authenticated': user_is_authenticated,
            'authenticated_user_contest_type': autenticated_user_data.get("contest_type"),
            'site_name': project_constants.SITE_NAME,
            'logged_user_id': logged_user_id,
    }
