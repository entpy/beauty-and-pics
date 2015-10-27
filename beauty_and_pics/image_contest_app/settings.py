# -*- coding: utf-8 -*-

"""
Django settings for image_contest_app app.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ICA_LIKE_LIMIT = 500 # like limit to close photo contest
ICA_CONTEST_ENABLED = True # check if init photo contest (True) or not (False)
ICA_CONTEST_TYPE_ACTIVE = 0 # 0 active for votation
ICA_CONTEST_TYPE_CLOSED = 1 # closed, image will be shown in catwalk
ICA_CONTEST_TYPE_FINISHED = 2 # finished, data was saved into ImageContestHallOfFame
