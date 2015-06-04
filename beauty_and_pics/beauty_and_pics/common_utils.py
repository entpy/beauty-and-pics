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
            if request.META["REMOTE_ADDR"]:
                return_var = request.META["REMOTE_ADDR"]
            elif request.META["HTTP_X_FORWARDED_FOR"]:
                return_var = request.META["HTTP_X_FORWARDED_FOR"]
        logger.info("indirizzo ip rilevato: " + str(return_var))

        return return_var
