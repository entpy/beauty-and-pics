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

class AccountEditForm(forms.Form, FormCommonUtils):

    first_name = forms.CharField(label='Nome', max_length=20, required=True, initial='Prova')
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', required=True)
    birthday_month = forms.ChoiceField(label='Mese', required=True)
    birthday_year = forms.ChoiceField(label='Anno', required=True)
    gender = forms.ChoiceField(label='Sesso', required=True)
    email = forms.CharField(label='Email', max_length=75, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    hair = forms.ChoiceField(label="Capelli", required=False) 
    eyes = forms.ChoiceField(label="Occhi", required=False)
    height = forms.CharField(label="Altezza (cm)", max_length=3, required=False)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
        'check_user_is_adult',
	'check_email_already_exists',
	'check_email_is_valid',
    )
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
        super(AccountEditForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(AccountEditForm, self)

        # setting addictional data to form fields
        self.fields["birthday_day"].choices=self.get_days_select_choices()
        self.fields["birthday_month"].choices=self.get_months_select_choices()
        self.fields["birthday_year"].choices=self.get_years_select_choices()
        self.fields["gender"].choices=self.get_genders_select_choices()
        self.fields["hair"].choices=self.get_hair_select_choices()
        self.fields["eyes"].choices=self.get_eyes_select_choices()

    def clean(self):
	super(AccountEditForm, self).clean_form_custom()
        return True

    def save_form(self):
        return_var = False
        if super(AccountEditForm, self).form_can_be_saved():
            account_obj = Account()

	    # setting addictional fields
	    # building birthday date
            birthday_date = account_obj.create_date(date_dictionary={"day" : self.form_validated_data.get("birthday_day"), "month" : self.form_validated_data.get("birthday_month"), "year" : self.form_validated_data.get("birthday_year")}, get_isoformat=True)
	    if (birthday_date):
                self.form_validated_data["birthday_date"] = birthday_date

            # saving new account
            try:
                # TODO update data about this account
                # account_obj.register_account(user_info=self.form_validated_data)
                return_var = True
            except UserCreateError:
                # bad
                logger.error("Errore nel salvataggio del nuovo User e/o Account: " + str(self.form_validated_data) + " | error code: " + str(UserCreateError.get_error_code))
                self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserCreateError.get_error_code) + ")"]}
            except UserUpdateDataError:
                # bad
                logger.error("Errore nell'aggiornamento dei dati dell'account dopo la creazione: " + str(self.form_validated_data) + " | error code: " + str(UserUpdateDataError.get_error_code))
                self._errors = {"__all__": ["Errore nel salvataggio del tuo account. Sii gentile, segnala il problema (Codice " + str(UserUpdateDataError.get_error_code) + ")"]}
            else:
                logger.info("Utente salvato con successo, preparo il login")
                pass

        return return_var

    def form_actions(self):
        """Function to create new user and logging into website"""
        return_var = False

        if self.save_form():
            return_var = True

        return return_var
