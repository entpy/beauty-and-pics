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

class LoginForm(forms.Form, FormCommonUtils):

    email = forms.CharField(label='Email', max_length=75, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )

    # list of addictional validator fied
    addictional_validation_fields = {}

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(LoginForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(LoginForm, self)

    def clean(self):
	super(LoginForm, self).clean_form_custom()
        return True

    def log_user_in(self):
        """Function to create a login session"""
        return_var = False
        try:
            # retrieving validated email and password, then try to log user in
            account_obj = Account()
            email = self.form_validated_data["email"]
            password = self.form_validated_data["password"]
            login_status = account_obj.create_login_session(email=email, password=password, request=self.request_data)
        except UserNotActiveError:
            # bad
            logger.error("Errore nel login: utente non attivo " + str(self.form_validated_data) + " | error code: " + str(UserNotActiveError.get_error_code))
            self._errors = {"__all__": ["Caspita, il tuo account è stato bloccato...AHAH"]}
        except UserLoginError:
            # bad
            logger.error("Errore nel login: email o password non validi " + str(self.form_validated_data) + " | error code: " + str(UserLoginError.get_error_code))
            self._errors = {"__all__": ["Email o password non validi, prova ancora"]}
        else:
            return_var = True
            logger.info("Login avvenuto con successo: " + str(self.form_validated_data))

        return return_var

    def form_actions(self):
        return_var = False
        if (super(LoginForm, self).form_can_perform_actions()):
            # try to log user in
            if self.log_user_in():
                return_var = True

        return return_var
