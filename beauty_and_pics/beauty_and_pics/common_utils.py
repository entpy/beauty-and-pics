# common utils object
from contest_app.models.contests import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CommonUtils(object):
    def get_ip_address(self, request):
        """Function to retrieve ip address"""
        return_var = None

        if request:
            if request.META.get("REMOTE_ADDR"):
                return_var = request.META.get("REMOTE_ADDR")
            elif request.META.get("HTTP_X_FORWARDED_FOR"):
                return_var = request.META.get("HTTP_X_FORWARDED_FOR")
        logger.info("indirizzo ip rilevato: " + str(return_var))

        return return_var
