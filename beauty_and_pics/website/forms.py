from django import forms
from datetime import date
from dateutil.relativedelta import *
import calendar, logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class FormCommonUtils():

    # list of valid validation methods
    valid_custom_validation_list = ('all_fields_valid', 'user_is_adult',)
    # list of custom validation methods, eg. ('all_fields_valid', 'another_method',)
    custom_validation_list = ()
    # adductional fields used in validation methods
    addictional_validation_fields = {}
    # TODO: use this field to add errors
    validation_errors = {}
    # form to validate instance
    validation_form = False
    # valid data retrieved after method "all_fields_valid"
    form_validated_data = False

    def __init__(self, *args, **kwargs):
        # custom_validation_list = False, addictional_validation_fields = False, validation_form = False
        # setting form validation list
        if custom_validation_list:
            for validation in custom_validation_list:
                # a method will be used only if exists inside 
                # "valid_custom_validation_list" list
                if self.check_if_validation_method_is_valid(validation):
                    self.custom_validation_list + (validation,)
        # setting form addictional validation fields
        if addictional_validation_fields:
            self.addictional_validation_fields = addictional_validation_fields

        # setting form instance
        if validation_form:
            self.validation_form = validation_form

    def check_if_validation_method_is_valid(self, validation_method = False):
        """Checking if a validation method exists"""
        return validation_method in self.valid_custom_validation_list

    def clean_form_custom(self):
        """Running all validation functions"""
        if self.custom_validation_list:
            cont = 0
            for validation in self.custom_validation_list:
                logger.debug(str(cont) + " metodo: " + str(validation))
                exec("self." + validation + "()")
                cont += 1

        return True

    ##########################
    ##  validation methods  ##
    ##########################

    def all_fields_valid(self):
        """Validation method to check if all fields are valid"""
        form_is_valid = self.validation_form.is_valid()
        if not form_is_valid:
            self.add_error(None, "Ricontrolla i tuoi dati")

        # inserisco i valori validi
        self.form_validated_data = self.validation_form.clean()

        return True

    def user_is_adult(self):
        """Validation method to check if a user is adult"""
        birthday_dictionary = {
            "birthday_year" : self.form_validated_data.get(self.addictional_validation_fields["year"]),
            "birthday_month" : self.form_validated_data.get(self.addictional_validation_fields["month"]),
            "birthday_day" : self.form_validated_data.get(self.addictional_validation_fields["day"]),
        }

        if (not self.check_if_user_is_adult(birthday_dictionary=birthday_dictionary)):
            # raise an exception if user is not adult
            self.add_error(None, "Per continuare devi essere maggiorenne")
            self.add_error(self.addictional_validation_fields["year"], True)
            self.add_error(self.addictional_validation_fields["month"], True)
            self.add_error(self.addictional_validation_fields["day"], True)

        return True

    ##########################
    ##     other stuff      ##
    ##########################

    def get_days_select_choices(self):
        """Create a list of days for select element"""
        select_choices = []
        for i in range(1,32):
                select_choices.append((i, i))
        return select_choices

    def get_months_select_choices(self):
        """Create a list of months for select element"""
        select_choices = []
        for i in range(1,13):
                select_choices.append((i, calendar.month_name[i]))
        return select_choices

    def get_years_select_choices(self):
        """Create a list of years for select element"""
        #                   current year - 18
        #                           |
        #                           V
        select_choices = []
        #for i in range(1960, (date.today().year - 17)):
        for i in range(1960, (date.today().year - 10)):
                select_choices.append((i, i))
        return select_choices

    def get_genders_select_choices(self):
        """Create a list of genders for select element"""
        select_choices = []
        select_choices.append(("f", "Donna"))
        select_choices.append(("m", "Uomo"))
        return select_choices

    def check_if_user_is_adult(self, birthday_dictionary):
        """Check if a user is adult or not.
        Return: true on success, false otherwise"""

        return_var = False
        birthday_year = int(birthday_dictionary.get("birthday_year", 0))
        birthday_month = int(birthday_dictionary.get("birthday_month", 0))
        birthday_day = int(birthday_dictionary.get("birthday_day", 0))

        if (birthday_year and birthday_month and birthday_day):
            # date(yy/mm/dd)
            today_date=date(year=date.today().year,month=date.today().month,day=date.today().day)
            birthday_date=date(year=birthday_year,month=birthday_month,day=birthday_day)

            # diff between two dates
            diff_between_dates = relativedelta(today_date, birthday_date)
            if (diff_between_dates.years >= 18):
                # user is adult
                return_var = True
        return return_var



class RegisterForm(forms.Form, FormCommonUtils):

    first_name = forms.CharField(label='Nome', max_length=20, required=True)
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', required=True)
    birthday_month = forms.ChoiceField(label='Mese', required=True)
    birthday_year = forms.ChoiceField(label='Anno', required=True)
    gender = forms.ChoiceField(label='Sesso', required=True)
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

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

        # parent FormCommonUtils  init
        FormCommonUtils.__init__(self, custom_validation_list = self.custom_validation_list, addictional_validation_fields = self.addictional_validation_fields, validation_form = super(RegisterForm, self))

        # setting addicitonal data to form fields
        self.fields["birthday_day"].choices=self.get_days_select_choices()
        self.fields["birthday_month"].choices=self.get_months_select_choices()
        self.fields["birthday_year"].choices=self.get_years_select_choices()
        self.fields["gender"].choices=self.get_genders_select_choices()

    def clean(self):
	super(RegisterForm, self).clean_form_custom()
        return True
