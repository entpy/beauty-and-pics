from django import forms
from datetime import date
from dateutil.relativedelta import *
import calendar, logging
from custom_form_app.forms.base_form_class import *
from account_app.models import *

# Get an instance of a logger
logger = logging.getLogger('django.request')

class RegisterForm(forms.Form, FormCommonUtils):

    first_name = forms.CharField(label='Nome', max_length=20, required=True)
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', required=True)
    birthday_month = forms.ChoiceField(label='Mese', required=True)
    birthday_year = forms.ChoiceField(label='Anno', required=True)
    gender = forms.ChoiceField(label='Sesso', required=True)
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

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

    def save(self):
        return_var = False
        if super(RegisterForm, self).get_validation_errors_status() is False:
            account_obj = Account()
	    # building birthday date
	    # fare una funzione sotto account per calcolare la data di nascita ed utilizzarla anche in custom form base
            birthday_day = self.form_validated_data.get("birthday_day")
            birthday_month = self.form_validated_data.get("birthday_month")
            birthday_year = self.form_validated_data.get("birthday_year")

	    # TODO password must be encripted

	    # delete last_name key from dictionary if is empty
            if (not self.form_validated_data["last_name"]):
	        del self.form_validated_data["last_name"]

	    # setting addictional fields
	    if (birthday_day and birthday_month and birthday_year):
                self.form_validated_data["birthday_date"] = date(year=int(birthday_year), month=int(birthday_month), day=int(birthday_day)).isoformat()
            self.form_validated_data["status"] = 1

	    # saving data inside account model
            account_obj.save_data(save_data=(self.form_validated_data))
            return_var = True
        return return_var
