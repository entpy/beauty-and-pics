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
    MAN_CONTEST = "man_contest"

    WOMAN_CONTEST = "woman_contest"
    # contest types }}}

    # account gender {{{
    MAN_GENDER = "man"

    WOMAN_GENDER = "woman"
    # account gender }}}

    # contest details {{{
    # CONTEST_OPENING_DAYS = 35
    # XXX: debug, use this instead --^
    CONTEST_OPENING_DAYS = 3

    CONTEST_EXPIRING_DAYS = 330
    # contest details }}}

    # catwalk user group name
    CATWALK_GROUP_NAME = "catwalk_user"

    # votations {{{
    # vote seconds min limit
    SECONDS_BETWEEN_VOTATION = 172800 # 172800 seconds = 2 days

    VOTE_METRICS_LIST = {"global_metric": "global", "smile_metric": "smile", "look_metric": "look"}

    IMAGE_TYPE = {"profile": "profile_image", "book": "book_image"}

    # votations }}}

    # newsletters bitmask {{{
    WEEKLY_REPORT_EMAIL_BITMASK = 1
    CONTEST_REPORT_EMAIL_BITMASK = 2

    SITE_NAME = "Beauty and Pics"
    # newsletters bitmask }}}
