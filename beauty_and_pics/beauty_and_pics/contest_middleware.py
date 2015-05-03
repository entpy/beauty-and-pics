# middleware to manage contest, expiring date and ranking block
from contest_app.models.contests import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ContestMiddleware(object):
    def process_request(self, request):
        contest_obj = Contest()
        # contest manager function
        contest_obj.contest_manager()
