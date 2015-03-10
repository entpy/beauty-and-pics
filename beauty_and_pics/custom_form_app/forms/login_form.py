# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
from account_app.models import *
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger('django.request')

class LoginForm(forms.Form, FormCommonUtils):

    email = forms.CharField(label='Email', max_length=75, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

    # addictional request data
    request_data = None
    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )
    addictional_validation_fields = {}

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(LoginForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

        # setting current request (used to log the user in)
        self.request_data = request

	# current form instance
        self.validation_form = super(LoginForm, self)

    def clean(self):
	super(LoginForm, self).clean_form_custom()
        return True

    def form_actions(self):
        return_var = False
        if (super(LoginForm, self).form_can_be_saved() and self.request_data):

            # retrieving validated email and password
            email = self.form_validated_data["email"]
            password = self.form_validated_data["password"]

            account_obj = Account()
            login_status = account_obj.create_login_session(email=email, password=password, request=self.request_data)

            if login_status == True:
                return_var = True
            else:
                super(LoginForm, self).add_validation_error(error_msg=login_status)

        return return_var
