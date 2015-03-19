# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from django.contrib.auth.models import User
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
	'check_email_is_valid',
	'check_email_already_exists',
    )

    # list of addictional validator fied
    addictional_validation_fields = {
        "current_password":"current_password",
        "email":"email",
    }

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
        if super(Area51Form, self).form_can_perform_actions():
            # update user email and password
            account_obj = Account()
            try:
                account_obj.update_email_password(
                    current_email=self.request_data.user.email,
                    new_email=self.form_validated_data.get("email"),
                    password=self.form_validated_data.get("password")
                )
            except User.DoesNotExist:
                logger.error("Errore nell'aggiornamento email e password (utente non esistente): " + str(self.form_validated_data))
                self._errors = {"__all__": ["Errore nell'aggiornamento email e/o password. Sii gentile, segnala il problema"]}
            except UserEmailPasswordUpdateError:
                logger.error("Errore nell'aggiornamento email e password: " + str(self.form_validated_data) + " | error code: " + str(UserEmailPasswordUpdateError.get_error_code))
                self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserEmailPasswordUpdateError.get_error_code) + ")"]}
            else:
                return_var = True

        return return_var

    def update_login_session(self):
        """Function to update created login session with new email and password"""
        return_var = False
        account_obj = Account()
        try:
            account_obj.create_login_session(
                email=self.form_validated_data.get("email"),
                password=self.form_validated_data.get("password"),
                request=self.request_data
            )
        except UserNotActiveError, UserLoginError:
            logger.error("Errore nell'aggiornamento email e password, non sono riuscito a ricreare la sessione di login: " + str(self.form_validated_data))
        else:
            return_var = True

        return return_var

    def form_actions(self):
        """Function to update user email and password"""
        return_var = False
        # update user emal and password
        if self.save_form():
            # create new login session
            if self.update_login_session():
                return_var = True

        return return_var
