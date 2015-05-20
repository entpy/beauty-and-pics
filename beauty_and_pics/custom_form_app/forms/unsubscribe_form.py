# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from django.contrib.auth.models import User
from email_template.email.email_template import *
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
import logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UnsubscribeForm(forms.Form, FormCommonUtils):

    receive_weekly_report = forms.BooleanField(label='Voglio ricevere il report settimanale')
    contest_report = forms.BooleanField(label='Voglio ricevere il report annuale del concorso')

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(UnsubscribeForm, self)

    def clean(self):
	super(UnsubscribeForm, self).clean_form_custom()
        return True

    def manage_newsletters(self):
        """Function to unsubscribe/subscribe user"""
        # unsubscribe user
        account_obj = Account()
        if self.form_validated_data["receive_weekly_report"]:
            # TODO: add weekly report bitmask
            pass
        else:
            # TODO: remove weekly report bitmask
            pass

        if self.form_validated_data["contest_report"]:
            # TODO: add contest report bitmask
            pass
        else:
            # TODO: remove contest report bitmask
            pass

        return True

    def form_actions(self):
        """Function to perform form action"""
        return_var = False
        if super(UnsubscribeForm, self).form_can_perform_actions():
            if self.manage_newsletters():
                return_var = True

        return return_var
