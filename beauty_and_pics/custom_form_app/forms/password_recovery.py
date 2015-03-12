# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
from django.contrib.auth.models import User
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class passwordRecoveryForm(forms.Form, FormCommonUtils):

    email = forms.CharField(label='Email', max_length=75, required=True)

    # addictional request data
    request_data = None

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )
    addictional_validation_fields = {}

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(passwordRecoveryForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(passwordRecoveryForm, self)

    def clean(self):
	super(passwordRecoveryForm, self).clean_form_custom()
        return True

    def form_actions(self):
        return_var = False
        if (super(passwordRecoveryForm, self).form_can_be_saved()):

            account_obj = Account()
            # retrieving user by email
            email = self.form_validated_data["email"]

            # generate user password
	    new_password = account_obj.generate_new_password()

	    # update user with new password
            try:
	        account_obj.update_user_password(email=email, new_password=new_password)
            except User.DoesNotExist:
                logger.error("Errore nel recupero password: utente non esistente" + str(self.form_validated_data))
                self._errors = {"__all__": ["Sembrerebbe che l'email inserita non esista"]}

	    # TODO: send new password via email

            logger.info("nuova password generata (" + str(new_password) + ") per: " + str(self.form_validated_data))

        return return_var
