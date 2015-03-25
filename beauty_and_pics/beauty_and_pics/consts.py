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

    # contest details {{{
    # CONTEST_OPENING_DAYS = 35
    # XXX: debug, use this instead --^
    CONTEST_OPENING_DAYS = 3

    CONTEST_EXPIRING_DAYS = 330
    # contest details }}}

    # catwalk user group name
    CATWALK_GROUP_NAME = "catwalk_user"
