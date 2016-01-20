# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
from email_template.email.email_template import *
from account_app.models import *
from website.exceptions import *
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class RegisterForm(forms.Form, FormCommonUtils):

    first_name = forms.CharField(label='Nome', max_length=20, required=True)
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', required=True)
    birthday_month = forms.ChoiceField(label='Mese', required=True)
    birthday_year = forms.ChoiceField(label='Anno', required=True)
    gender = forms.ChoiceField(label='Sesso', required=True)
    email = forms.CharField(label='Email (valida)', max_length=75, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
        'check_user_is_adult',
	'check_email_already_exists',
	'check_email_is_valid',
    )

    # list of addictional validator fied
    addictional_validation_fields = {
        "year":"birthday_year",
        "month":"birthday_month",
        "day":"birthday_day",
        "email":"email",
    }

    # addictional request data
    request_data = None

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(RegisterForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(RegisterForm, self)

        # setting addictional data to form fields
        self.fields["birthday_day"].choices=self.get_days_select_choices()
        self.fields["birthday_month"].choices=self.get_months_select_choices()
        self.fields["birthday_year"].choices=self.get_years_select_choices()
        self.fields["gender"].choices=self.get_genders_select_choices()

    def clean(self):
	super(RegisterForm, self).clean_form_custom()
        return True

    def save_form(self):
        return_var = False
        account_obj = Account()
        # setting addictional fields
        # building birthday date
        birthday_date = account_obj.create_date(date_dictionary={"day" : self.form_validated_data.get("birthday_day"), "month" : self.form_validated_data.get("birthday_month"), "year" : self.form_validated_data.get("birthday_year")}, get_isoformat=True)
        if (birthday_date):
            self.form_validated_data["birthday_date"] = birthday_date

        # saving new account
        try:
	    self.form_validated_data["status"] = 1

	    # uppercase first name and last name
	    self.form_validated_data["first_name"] = self.form_validated_data["first_name"].title()
	    self.form_validated_data["last_name"] = self.form_validated_data["last_name"].title()
            # generate auth token
            self.form_validated_data["auth_token"] = account_obj.create_auth_token(email=self.form_validated_data["email"])

            account_obj.register_account(user_info=self.form_validated_data)
        except UserCreateError:
            # bad
            logger.error("Errore nel salvataggio del nuovo User e/o Account: " + str(self.form_validated_data) + " | error code: " + str(UserCreateError.get_error_code))
            self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserCreateError.get_error_code) + ")"]}
        except UserUpdateDataError:
            # bad
            logger.error("Errore nell'aggiornamento dei dati dell'account dopo la creazione: " + str(self.form_validated_data) + " | error code: " + str(UserUpdateDataError.get_error_code))
            self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserUpdateDataError.get_error_code) + ")"]}
        else:
            logger.info("Utente salvato con successo, invio la mail con token di conferma")
            # send email with activation key
            self.send_activation_email()
            return_var = True

        return return_var

    def send_activation_email(self):
        """Function to send an activation email"""

        email_context = {
            "first_name": self.form_validated_data["first_name"],
            "last_name": self.form_validated_data["last_name"],
            "auth_token": self.form_validated_data["auth_token"],
        }
        CustomEmailTemplate(
            email_name="user_activate_email",
            email_context=email_context,
            template_type="user",
            recipient_list=[self.form_validated_data["email"],]
        )

        return True

    def log_user(self):
        """Function to create login session"""
        return_var = False

        # retrieving validated email and password, then try to log user in
        email = self.form_validated_data["email"]
        password = self.form_validated_data["password"]

        try:
            account_obj = Account()
            login_status = account_obj.create_login_session(email=email, password=password, request=self.request_data)
        except UserNotActiveError:
            # bad
            logger.error("Errore nel login: utente non attivo " + str(self.form_validated_data) + " | error code: " + str(UserNotActiveError.get_error_code))
            self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserNotActiveError.get_error_code) + ")"]}
        except UserLoginError:
            # bad
            logger.error("Errore nel login: email o password non validi " + str(self.form_validated_data) + " | error code: " + str(UserLoginError.get_error_code))
            self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserLoginError.get_error_code) + ")"]}
        else:
            # new user successfully logged in
            return_var = True

        return return_var

    def form_actions(self):
        """Function to create new user and logging into website"""
        return_var = False
        if super(RegisterForm, self).form_can_perform_actions():
            # try to save form data
            if self.save_form():
                # send welcome email
                # self.send_welcome_email()
                # try to log user in
                if self.log_user():
                    return_var = True

        return return_var
