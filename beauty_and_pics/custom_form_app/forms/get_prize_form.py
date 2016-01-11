# -*- coding: utf-8 -*-

from django import forms
from custom_form_app.forms.base_form_class import *
from account_app.models import *
from website.exceptions import *
from email_template.email.email_template import *
from beauty_and_pics.consts import project_constants
import calendar, logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GetPrizeForm(forms.Form, FormCommonUtils):

    address = forms.CharField(label='Indirizzo', max_length=100, required=True)
    size = forms.ChoiceField(label='Taglia', required=True)
    note = forms.CharField(label='Note aggiuntive', max_length=300, required=False)

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )

    # list of addictional validator fied
    addictional_validation_fields = { }

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(GetPrizeForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(GetPrizeForm, self)

        # setting addictional data to form fields
        self.fields["size"].choices=self.get_size_for_select()

    def clean(self):
	super(GetPrizeForm, self).clean_form_custom()
        return True

    def form_actions(self):
        """Function to perform form actions"""
        return_var = False
        if super(GetPrizeForm, self).form_can_perform_actions():
            account_obj = Account()

            # send email to admin with prize info
            self.send_email()

            # update account info (prize is now redeemed)
            self.form_validated_data["prize_status"] = project_constants.PRIZE_ALREADY_REDEEMED
            account_obj.update_data(save_data=self.form_validated_data, user_obj=self.request_data.user)

            return_var = True

        return return_var

    """
    Custom form functions
    """
    def get_size_for_select(self):
        """Create a list of size for select element"""
        select_choices = []
        select_choices.append(("s", "S"))
        select_choices.append(("m", "M"))
        select_choices.append(("l", "L"))

        return select_choices

    def send_email(self):
        # send email to admin
        email_context = { 
            "user_email": self.request_data.user.email,
            "user_id": self.request_data.user.id,
            "user_profile_url": settings.SITE_URL + "/passerella/dettaglio-utente/" + str(self.request_data.user.id) + "/",
            "address": self.form_validated_data.get("address"),
            "size": self.form_validated_data.get("size"),
            "note": self.form_validated_data.get("note"),
        }
        CustomEmailTemplate(
	    email_name="get_prize_email",
	    email_context=email_context,
	    template_type="user",
	    email_from=self.request_data.user.email,
	)

        return True
