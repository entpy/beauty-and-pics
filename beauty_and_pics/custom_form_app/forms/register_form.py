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
        'all_fields_valid',
        'user_is_adult',
    )
    addictional_validation_fields = {
        "year":"birthday_year",
        "month":"birthday_month",
        "day":"birthday_day",
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

    def actions(self):
        return_var = False
        if super(RegisterForm, self).get_validation_errors_status() is False:
            # save data inside model
            account_obj = Account()
            account_obj.first_name = self.form_validated_data["first_name"]
            account_obj.last_name = self.form_validated_data["last_name"]
            account_obj.email = self.form_validated_data["email"]
            account_obj.password = self.form_validated_data["password"]
            account_obj.gender = self.form_validated_data["gender"]
            account_obj.status = 1
            # account_obj.birthday_date = self.cleaned_data["first_name"]

            account_obj.save()

            return_var = True

        return return_var
