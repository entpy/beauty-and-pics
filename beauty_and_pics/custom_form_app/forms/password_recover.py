# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
from email_template.email.email_template import *
from django.contrib.auth.models import User
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class passwordRecoverForm(forms.Form, FormCommonUtils):

    email = forms.CharField(label='Email', max_length=75, required=True)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )

    # list of addictional validator fied
    addictional_validation_fields = {}

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(passwordRecoverForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(passwordRecoverForm, self)

    def clean(self):
	super(passwordRecoverForm, self).clean_form_custom()

        return True

    def generate_new_password(self):
        """Function to genereate a new password"""
        return_var = False
        try:
            # generate a new password
            account_obj = Account()
            new_password = account_obj.generate_new_password()
            account_obj.update_email_password(current_email=self.form_validated_data["email"], password=new_password)
        except User.DoesNotExist:
            logger.error("Errore nel recupero password: utente non esistente" + str(self.form_validated_data))
            self._errors = {"__all__": ["Sembrerebbe che l'email inserita non esista"]}
        except UserEmailPasswordUpdateError:
            logger.error("Errore nel recupero password: " + str(self.form_validated_data) + " | error code: " + str(UserEmailPasswordUpdateError.get_error_code))
            self._errors = {"__all__": ["Errore nel recupero password. Sii gentile, segnala il problema (Codice " + str(UserEmailPasswordUpdateError.get_error_code) + ")"]}
        else:
            logger.info("nuova password generata (" + str(new_password) + ") per: " + str(self.form_validated_data))
            return_var = new_password

        return return_var

    def send_password_email(self, new_password=None):
        """Function to send generated password via email"""
        return_var = False
	# retrieve account info
	account_obj = Account()
        try:
	    user_obj = account_obj.get_user_about_email(email=self.form_validated_data["email"])
        except User.DoesNotExist:
            logger.error("Errore nel recupero password: utente non esistente" + str(self.form_validated_data))
            self._errors = {"__all__": ["Sembrerebbe che l'email inserita non esista"]}
	else:
	    # retrieving first name and last name
	    # account_obj.custom_user_id_data(user_id=user_obj.id):
	    # send new password via email
	    email_context = { "first_name" : user_obj.first_name, "last_name" : user_obj.last_name, "email": self.form_validated_data["email"], "password": new_password }
	    CustomEmailTemplate(
		email_name="recover_password_email",
		email_context=email_context,
		template_type="user",
		recipient_list=[self.form_validated_data["email"],]
	    )
	    return_var = True

        return return_var

    def form_actions(self):
        return_var = False
        if (super(passwordRecoverForm, self).form_can_perform_actions()):
            # generate a new password
            new_password = self.generate_new_password()
            if new_password:
                # send generated password via mail
                self.send_password_email(new_password=new_password)
                return_var = True

        return return_var
