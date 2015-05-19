# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import *
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

class ReportUserForm(forms.Form, FormCommonUtils):

    email = forms.CharField(label='La tua email', max_length=75, required=True)
    report_user_id = forms.IntegerField(required=True)
    report_text = forms.CharField(label='Dettagli segnalazione', max_length=1000, required=True, widget=forms.Textarea)

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
        super(ReportUserForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(ReportUserForm, self)

    def clean(self):
	super(ReportUserForm, self).clean_form_custom()
        return True

    def send_email(self):
        account_obj =  Account()
        return_var = False
        try:
            # retrieve report user data
            account_info = account_obj.custom_user_id_data(user_id=self.form_validated_data["report_user_id"])
        except Account.DoesNotExist:
            # wtf: user id doesn't exists
            pass
        else:
            # send report user email
            email_context = {
                "email": self.form_validated_data["email"],
                "report_text": self.form_validated_data["report_text"],
                "report_user_id": self.form_validated_data["report_user_id"],
                "report_user_email": account_info["email"],
                "report_user_profile_url": settings.SITE_URL + "/passerella/dettaglio-utente/" + str(self.form_validated_data["report_user_id"]) + "/",
            }

            CustomEmailTemplate(
                email_name="report_user_email",
                email_context=email_context,
                template_type="user",
                email_type="admin_email",
            )
            return_var = True

        return return_var

    def form_actions(self):
        """Function to update user email and password"""
        return_var = False
        if super(ReportUserForm, self).form_can_perform_actions():
            # send help mail 
            if self.send_email():
                return_var = True

        return return_var
