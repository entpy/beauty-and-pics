# -*- coding: utf-8 -*-

"""
In this module will be defined all constanst about Beauty & Pics
"""
class project_constants(object):
    # contest status {{{
    CONTEST_OPENING = "opening"
    CONTEST_ACTIVE = "active"
    CONTEST_CLOSED = "closed"
    # contest status }}}

    # contest types {{{
    MAN_CONTEST = "man-contest"
    WOMAN_CONTEST = "woman-contest"
    # contest types }}}

    # account gender {{{
    MAN_GENDER = "man"
    WOMAN_GENDER = "woman"
    # account gender }}}

    # prize consts {{{
    PRIZE_CANNOT_BE_REDEEMED = 0
    PRIZE_CAN_BE_REDEEMED = 1
    PRIZE_ALREADY_REDEEMED = 2
    # prize consts }}}

    # contest details {{{
    # see here -> http://www.epochconverter.com/epoch/daynumbers.php
    # CONTEST_OPENING_DAYS = 35
    # XXX: debug, use this instead --^
    CONTEST_OPENING_DAYS = 30
    CONTEST_EXPIRING_DAYS = 165
    # contest details }}}

    # catwalk user group name
    CATWALK_GROUP_NAME = "catwalk_user"

    # votations {{{
    # vote seconds min limit
    SECONDS_BETWEEN_VOTATION = 604800 # 604800 seconds = 7 days

    VOTE_METRICS_LIST = {"smile_metric": "smile", "look_metric": "look", "global_metric": "global", "style_metric": "style"}

    IMAGE_TYPE = {"profile": "profile_image", "book": "book_image"}

    # votations }}}

    # newsletters bitmask {{{
    WEEKLY_REPORT_EMAIL_BITMASK = 1
    CONTEST_REPORT_EMAIL_BITMASK = 2

    SITE_NAME = "Beauty and Pics"

    # cookie naming: _bp_firstletter_
    USER_ALREADY_VOTED_COOKIE_NAME = "_uav_"

    USER_NOTIFY_POPUP_SHOWN_COOKIE_NAME = "_bp_unpsk_"
    USER_NOTIFY_POPUP_SHOWN_COOKIE_EXPIRING_SECONDS = 60*60 # cookie expiring in seconds (60s * 60m = 1 hour)
    # newsletters bitmask }}}
