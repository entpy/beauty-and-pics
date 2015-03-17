# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
from website.email.email_template import *
from django.contrib.auth.models import User
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class passwordRecoverForm(forms.Form, FormCommonUtils):

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
        super(passwordRecoverForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(passwordRecoverForm, self)

    def clean(self):
	super(passwordRecoverForm, self).clean_form_custom()
        return True

    def form_actions(self):
        return_var = False
        if (super(passwordRecoverForm, self).form_can_be_saved()):
            try:
                account_obj = Account()
                # generate user password
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
                # send new password via email
                custom_email_template_obj = CustomEmailTemplate()
                custom_email_template_obj.template_name = "recover_password"
                custom_email_template_obj.email_subject = "Beauty & Pics: recupero password!"
                custom_email_template_obj.email_context = {"email": self.form_validated_data["email"], "password": new_password}
                custom_email_template_obj.send_mail()

                return_var = True

        return return_var
