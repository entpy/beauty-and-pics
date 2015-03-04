from django import forms
from datetime import date
from dateutil.relativedelta import *
import calendar, logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class FormCommonUtils():

    # list of valid validation methods
    valid_custom_validation_list = ()
    # list of custom validation methods, eg. ('all_fields_valid', 'another_method',)
    custom_validation_list = ()
    # adductional fields used in validation methods
    addictional_validation_fields = {}
    # use this field to add errors
    _validation_errors = False
    # valid data retrieved after method "all_fields_valid"
    form_validated_data = False
    # flag to check if validation process is completed
    _validation_process_completed = False

    def __init__(self):
        # list of valid methods
	FormCommonUtils.valid_custom_validation_list += ('all_fields_valid',)
	FormCommonUtils.valid_custom_validation_list += ('user_is_adult',)

    def check_if_validation_method_is_valid(self, validation_method = False):
        """Checking if a validation method exists"""
        return validation_method in self.valid_custom_validation_list

    def clean_form_custom(self):
        """Running all validation functions"""
        if self.custom_validation_list:
            for validation in self.custom_validation_list:
		if self.check_if_validation_method_is_valid(validation_method = validation):
			exec("self." + validation + "()")
		else:
			logger.debug("method " + str(validation) + " is not a valid method")

        self.set_validation_process_status(True)
        return True

    def add_validation_error(self, type=None, error_msg=False):
        """Function to add a validation error to current form instance"""
        self.add_error(type, error_msg)
        self.set_validation_errors_status(True)

        return True

    def get_validation_errors_status(self):
        """Function to retrieve _validation_errors flag"""
        return FormCommonUtils._validation_errors

    def set_validation_errors_status(self, v = None):
        """Function to set _validation_errors flag"""
        if v is not None:
            FormCommonUtils._validation_errors = v
        return True

    def get_validation_process_status(self):
        """Function to retrieve _validation_process_completed flag"""
        return FormCommonUtils._validation_process_completed

    def set_validation_process_status(self, v = None):
        """Function to retrieve _validation_process_completed flag"""
        if v is not None:
            FormCommonUtils._validation_process_completed = v
        return True

    ##########################
    ##  validation methods  ##
    ##########################

    def all_fields_valid(self):
        """Validation method to check if all fields are valid"""
        form_is_valid = self.validation_form.is_valid()
        if not form_is_valid:
            self.add_validation_error(None, "Ricontrolla i tuoi dati")

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
            self.add_validation_error(None, "Per continuare devi essere maggiorenne")
            self.add_validation_error(self.addictional_validation_fields["year"], True)
            self.add_validation_error(self.addictional_validation_fields["month"], True)
            self.add_validation_error(self.addictional_validation_fields["day"], True)

        return True

    ##########################
    ##     other stuff      ##
    ##########################

    def get_validation_json_response(self):
        """Function to retrieve JSON response after form validation"""
        import json

        if self.get_validation_process_status() is True:
            data = [ { 'success' : True, 'form_data' : self.form_validated_data } ]
            data_string = json.dumps(data)

        logger.debug("json retrieved " + str(data_string))

        return True

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
        birthday_year = birthday_dictionary.get("birthday_year", 0)
        birthday_month = birthday_dictionary.get("birthday_month", 0)
        birthday_day = birthday_dictionary.get("birthday_day", 0)

        if not birthday_year:
		birthday_year = 0
        if not birthday_month:
		birthday_month = 0
        if not birthday_day:
		birthday_day = 0

        birthday_year = int(birthday_year)
        birthday_month = int(birthday_month)
        birthday_day = int(birthday_day)

	logger.debug("anno: " + str(birthday_year))
	logger.debug("mese: " + str(birthday_month))
	logger.debug("giorno: " + str(birthday_day))

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
