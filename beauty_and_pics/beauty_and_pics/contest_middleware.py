# -*- coding: utf-8 -*-

# middleware to manage contest, expiring date and ranking block
from contest_app.models.contests import *
from image_contest_app.models import *
# import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)

class ContestMiddleware(object):
    """
    queste funzioni vengono chiamate più volte:
     - al caricamento della pagina
     - per ogni chiamata AJAX
    """
    def process_request(self, request):
        contest_obj = Contest()
        ImageContest_obj = ImageContest()

        # contest manager function
        contest_obj.contest_manager()
        # image contest manager function
        ImageContest_obj.image_contest_manager()
