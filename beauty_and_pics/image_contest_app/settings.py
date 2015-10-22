# -*- coding: utf-8 -*-

"""
Django settings for image_contest_app app.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ICA_LIKE_LIMIT = 500 # like limit to close photo contest
ICA_CONTEST_TYPE_BEST_PHOTO = 'best_photo' # like limit to close photo contest

ICA_CONTEST_ENABLED = True # check if init photo contest (True) or not (False)
