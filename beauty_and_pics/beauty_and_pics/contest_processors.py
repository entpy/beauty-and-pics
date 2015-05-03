# contest processor to manage common vars
from account_app.models.accounts import *
from account_app.models.images import *
from contest_app.models.contests import *
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def common_contest_processors(request):
    """Common template context processor function"""
    account_obj =  Account()
    book_obj = Book()
    contest_obj = Contest()
    logger.info("@@@current contest_type: " + str(contest_obj.get_contest_type_from_session(request=request)))

    ### template context vars {{{ ###
    # top five user ranking
    top_five_account = account_obj.get_top_five_contest_user(contest_type=contest_obj.get_contest_type_from_session(request=request))
    # profile thumbnail image url
    profile_thumbnail_image_url = None
    # current contest start_time
    contest_info = contest_obj.get_contest_info_about_type(contest_type=contest_obj.get_contest_type_from_session(request=request))
    ### template context vars }}} ###

    autenticated_user_data = account_obj.get_autenticated_user_data(request=request)
    if autenticated_user_data.get("user_id"):
        # logger.debug("[TEMPLATE_PROCESSOR] user logged in (user id: " + str(autenticated_user_data["user_id"]) + ")")
        profile_thumbnail_image_url = book_obj.get_profile_thumbnail_image_url(user_id=autenticated_user_data["user_id"])
    else:
        # logger.debug("[TEMPLATE_PROCESSOR] user NOT logged in")
        pass

    return {
            'top_five_account': top_five_account,
            'profile_thumbnail_image_url': profile_thumbnail_image_url,
            'contest_info': contest_info,
    }
