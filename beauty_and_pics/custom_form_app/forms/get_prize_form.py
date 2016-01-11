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
        self.fields["size"].choices=self.get_size()

    def clean(self):
	super(GetPrizeForm, self).clean_form_custom()
        return True

    def save_form(self):
        return_var = False
        if super(GetPrizeForm, self).form_can_perform_actions():
	    self.form_validated_data.get("address")
	    self.form_validated_data.get("size")
	    self.form_validated_data.get("note")
            # TODO send email to admin with prize info
            return_var = True

        return return_var

    def form_actions(self):
        """Function to create new user and logging into website"""
        return_var = False
        if self.save_form():
            return_var = True

        return return_var

    """
    Custom form functions
    """
    def get_size(self):
        """Create a list of size for select element"""
        select_choices = []
        select_choices.append(("s", "S"))
        select_choices.append(("m", "M"))
        select_choices.append(("l", "L"))

        return select_choices
