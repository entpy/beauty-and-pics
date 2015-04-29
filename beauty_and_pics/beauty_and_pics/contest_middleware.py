# middleware to manage contest, expiring date and ranking block
from contest_app.models.contests import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ContestMiddleware(object):
    def process_request(self, request):
        """
        request.say_hi = "Hi!!"
        logger.debug("saluto")

        """
        Contest_obj = Contest()
        Contest_obj.contest_manager()
        request.say_hi = "Hi!!"

    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        #request = response = view_func(request, *view_args, **view_kwargs)
        request.session["say_hi"] = "Hi!!"

        return request
    """
