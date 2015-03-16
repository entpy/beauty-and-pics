# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Area51Form(forms.Form, FormCommonUtils):

    email = forms.CharField(label='Email', max_length=75, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    current_password = forms.CharField(label='Password corrente', max_length=100, required=True)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
        'check_current_password',
	'check_email_already_exists',
    )

    addictional_validation_fields = {
        "current_password":"current_password",
        "email":"email",
    }

    # addictional request data
    # request_data = None

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(Area51Form, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(Area51Form, self)

    def clean(self):
	super(Area51Form, self).clean_form_custom()
        return True

    def save_form(self):
        return_var = False
        if super(Area51Form, self).form_can_be_saved():
            account_obj = Account()
            account_obj.update_data(save_data=self.form_validated_data, user_obj=self.request_data.user)
            return_var = True

        return return_var

    def form_actions(self):
        """Function to update user email and password"""
        return_var = False

        if self.save_form():
            return_var = True

        return return_var
