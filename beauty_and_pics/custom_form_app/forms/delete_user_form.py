# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from django.contrib.auth.models import User
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
import logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class DeleteUserForm(forms.Form, FormCommonUtils):

    user_id = forms.IntegerField(label='User id', required=True)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(DeleteUserForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(DeleteUserForm, self)

    def clean(self):
	super(DeleteUserForm, self).clean_form_custom()
        return True

    def delete_user(self):
        """Function to delete user"""
        return_var = False
        logged_user_id = self.request_data.user.id
        user_id = self.form_validated_data.get("user_id")
        account_obj = Account()
        try:
            account_obj.delete_user(user_id=user_id, logged_user_id=logged_user_id)
        except UserDeleteDoesNotExistsError:
            logger.error("Errore nell'eliminazione dell'account, l'id utente non esiste: " + str(self.form_validated_data) + " | error code: " + str(UserDeleteDoesNotExistsError.get_error_code))
            self._errors = {"__all__": ["Errore nell'eliminazione dell'account. Sii gentile, segnala il problema (Codice " + str(UserDeleteDoesNotExistsError.get_error_code) + ")"]}
        except UserDeleteIdDoesNotMatchError:
            logger.error("Errore nell'eliminazione dell'account, l'id utente non matcha con l'id utente in sessione: " + str(self.form_validated_data) + " | error code: " + str(UserDeleteIdDoesNotMatchError.get_error_code))
            self._errors = {"__all__": ["Errore nell'eliminazione dell'account. Sii gentile, segnala il problema (Codice " + str(UserDeleteIdDoesNotMatchError.get_error_code) + ")"]}
        else:
            return_var = True

        return return_var

    def form_actions(self):
        """Function to perform form actions"""
        return_var = False
        # delete user and related data
        if self.delete_user():
            return_var = True

        return return_var
