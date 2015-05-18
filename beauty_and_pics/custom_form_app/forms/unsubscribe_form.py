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

    email = forms.CharField(label='La tua email', max_length=75, required=True)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
	'check_email_is_valid',
    )

    # list of addictional validator fied
    addictional_validation_fields = {
        "email":"email",
    }

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(UnsubscribeForm, self)

    def clean(self):
	super(UnsubscribeForm, self).clean_form_custom()
        return True

    def unsubscribe_email(self):
        """Function to unsubscribe user"""
        # unsubscribe user
        return_var = False
        account_obj = Account()
        user_email = self.form_validated_data["email"]
        try:
            # if user exists will be unsubscribed
            user_obj = account_obj.get_user_about_email(email=user_email)
        except User.DoesNotExist:
            pass
        else:
            # TODO: plz try it!
            # setting 'receive_newsletters' to '0'
            user_obj.account.receive_newsletters = 0
            user_obj.save()
            return_var = True

        return return_var

    def form_actions(self):
        """Function to perform form action"""
        return_var = False
        if super(UnsubscribeForm, self).form_can_perform_actions():
            # send help mail 
            if self.unsubscribe_email():
                return_var = True

        return return_var
