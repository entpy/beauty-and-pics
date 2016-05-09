# -*- coding: utf-8 -*-

# middleware to manage contest, expiring date and ranking block
from contest_app.models.contests import *
from django_photo_contest.models import PhotoContest
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
        photo_contest_obj = PhotoContest()

        # contest manager function
        contest_obj.contest_manager()
        photo_contest_obj._create_defaults()
