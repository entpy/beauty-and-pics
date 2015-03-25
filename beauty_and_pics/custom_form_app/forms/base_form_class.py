# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from account_app.models import *
from website.exceptions import *
from beauty_and_pics.consts import project_constants
import calendar, logging, json, sys, re

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger('django.request')

class FormCommonUtils():

    # list of valid validation methods
    __valid_custom_validation_list = ()
    # list of valid form class
    __valid_form_class_list = ()
    # list of custom validation methods, eg. ('check_all_fields_valid', 'another_method',)
    custom_validation_list = ()
    # adductional fields used in validation methods
    addictional_validation_fields = {}
    # use this field to add errors
    __validation_errors = False
    # valid data retrieved after method "check_all_fields_valid"
    form_validated_data = False
    # flag to check if validation process is completed
    __validation_process_completed = False
    # request_data, extended from form classes
    request_data = False

    def __init__(self):
        # list of valid methods
	FormCommonUtils.__valid_custom_validation_list += ('check_all_fields_valid',)
	FormCommonUtils.__valid_custom_validation_list += ('check_user_is_adult',)
	FormCommonUtils.__valid_custom_validation_list += ('check_email_already_exists',)
	FormCommonUtils.__valid_custom_validation_list += ('check_email_is_valid',)
	FormCommonUtils.__valid_custom_validation_list += ('check_current_password',)

        # list of valid form class
	FormCommonUtils.__valid_form_class_list += ('AccountEditForm',)
	FormCommonUtils.__valid_form_class_list += ('Area51Form',)
	FormCommonUtils.__valid_form_class_list += ('HelpRequestForm',)
	FormCommonUtils.__valid_form_class_list += ('LoginForm',)
	FormCommonUtils.__valid_form_class_list += ('passwordRecoverForm',)
	FormCommonUtils.__valid_form_class_list += ('RegisterForm',)

    def check_if_validation_method_is_valid(self, validation_method=False):
        """Checking if a validation method exists"""
        return validation_method in self.__valid_custom_validation_list

    def check_if_form_class_is_valid(self, form_class=False):
        """Checking if a form class exists"""
        return form_class in self.__valid_form_class_list

    def clean_form_custom(self):
        """Running all validation functions"""
        if self.custom_validation_list:
            for validation in self.custom_validation_list:
		if self.check_if_validation_method_is_valid(validation_method = validation):
                    code = compile("self." + validation + "()", '<string>', 'exec')
                    exec(code)
		else:
                    logger.error("method " + str(validation) + " is not a valid method")
        self.set_validation_process_status(True)

        return True

    def add_validation_error(self, type=None, error_msg=False):
        """Function to add a validation error to current form instance"""
        self.add_error(type, error_msg)
        self.set_validation_errors_status(True)

        return True

    def get_validation_errors_status(self):
        """Function to retrieve __validation_errors flag"""
        return self.__validation_errors

    def set_validation_errors_status(self, v=None):
        """Function to set __validation_errors flag"""
        if v is not None:
            self.__validation_errors = v

        return True

    def get_validation_process_status(self):
        """Function to retrieve __validation_process_completed flag"""
        return self.__validation_process_completed

    def set_validation_process_status(self, v=None):
        """Function to retrieve __validation_process_completed flag"""
        if v is not None:
            self.__validation_process_completed = v

        return True

    def form_can_perform_actions(self):
        """Function to check if a form can perform actions"""
        return_var = False
        if (not self.get_validation_errors_status()) and self.get_validation_process_status() and self.request_data:
            return_var = True

        return return_var

    def set_current_request(self, request=None):
        if request:
            self.request_data = request

        return True

    ##########################
    ##  validation methods  ##
    ##########################

    def check_all_fields_valid(self):
        """Validation method to check if all fields are valid"""
        form_is_valid = self.validation_form.is_valid()
        if not form_is_valid:
            self.add_validation_error(None, "Ricontrolla i tuoi dati")

        # inserisco i valori validi
        self.form_validated_data = self.validation_form.clean()

        return True

    def check_user_is_adult(self):
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

    def check_email_already_exists(self):
        """Validation method to check if an email already exists"""
        account_obj = Account()
        validated_email = self.form_validated_data.get(self.addictional_validation_fields["email"])
        # if form email is != from current logged in user email, checking if email exists or not
	if validated_email != account_obj.get_autenticated_user_email(self.request_data):
            if (account_obj.check_if_email_exists(email_to_check=validated_email) == True):
	        # raise an exception if email already exists
	        self.add_validation_error(None, "La mail \"" + str(validated_email) + "\" è già presente.")
                self.add_validation_error(self.addictional_validation_fields["email"], True)

        return True

    def check_current_password(self):
        """Validation method to check if a password match the user password"""
        account_obj = Account()
        validated_current_password = self.form_validated_data.get(self.addictional_validation_fields["current_password"])
        try:
            account_obj.check_user_password(request=self.request_data, password_to_check=validated_current_password)
        except UserPasswordMatchError:
            self.add_validation_error(None, "Per poter salvare le informazioni è necessario inserire la tua password attuale (corretta!)")
            self.add_validation_error(self.addictional_validation_fields["current_password"], True)

        return True

    def check_email_is_valid(self):
        """Validation method to check if an email is valid"""
        email_to_check = self.form_validated_data.get(self.addictional_validation_fields["email"])
	if email_to_check:
	    # regexp to check if this is a valid email
            match = re.search('^[a-zA-Z0-9_-][^@]*@(?:[^\.@]+\.)+[a-zA-Z0-9_-]+$', email_to_check)
            if match is None or not match.group(0):
	        self.add_validation_error(None, "La mail inserita non è valida")
                self.add_validation_error(self.addictional_validation_fields["email"], True)

        return True

    def check_if_user_is_adult(self, birthday_dictionary):
        """Check if a user is adult or not. Return: true on success, false otherwise"""
        return_var = False
        account_obj = Account()

        birthday_date = account_obj.create_date(date_dictionary={"day" : birthday_dictionary.get("birthday_day"), "month" : birthday_dictionary.get("birthday_month"), "year" : birthday_dictionary.get("birthday_year")})
        if birthday_date:
            # date(yy/mm/dd)
            today_date=date(year=date.today().year,month=date.today().month,day=date.today().day)

            # diff between two dates
            diff_between_dates = relativedelta(today_date, birthday_date)
            if (diff_between_dates.years >= 18):
                # user is adult
                return_var = True

        return return_var

    ##########################
    ##     other stuff      ##
    ##########################

    def get_validation_json_response(self):
        """Function to retrieve JSON response after form validation"""
        import json

        data = {}
        json_data_string = {}
        if self.get_validation_process_status() is True:
            if self.get_validation_errors_status() is True:
                data = {'error' : True,'form_data' : json.loads(self.validation_form.errors.as_json()) }
            else:
                data = {'success' : True,'form_data' : json.loads(self.validation_form.errors.as_json()) }
            json_data_string = json.dumps(data)

        # logger.debug("json retrieved " + str(data_string))

        return json_data_string

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
        #for i in range(1960, (date.today().year - 17)):
        select_choices = []
        for i in range(1960, (date.today().year - 10)):
                select_choices.append((i, i))

        return select_choices

    def get_genders_select_choices(self):
        """Create a list of genders for select element"""
        select_choices = []
        select_choices.append((project_constants.WOMAN_CONTEST, "Donna"))
        select_choices.append((project_constants.MAN_CONTEST, "Uomo"))

        return select_choices

    def get_hair_select_choices(self):
        """Create a list of hair color for select element"""
        select_choices = []
        select_choices.append(("", "-"))
        select_choices.append(("light_brown", "Castano chiaro"))
        select_choices.append(("dark_brown", "Castano scuro"))
        select_choices.append(("black", "Nero"))
        select_choices.append(("blond", "Biondo"))
        select_choices.append(("red", "Rosso"))

        return select_choices

    def get_eyes_select_choices(self):
        """Create a list of eyes color for select element"""
        select_choices = []
        select_choices.append(("", "-"))
        select_choices.append(("light_brown", "Marrone chiaro"))
        select_choices.append(("dark_brown", "Marrone scuro"))
        select_choices.append(("light_green", "Verde chiaro"))
        select_choices.append(("dark_green", "Verde scuro"))
        select_choices.append(("azure", "Azzurro"))

        return select_choices
