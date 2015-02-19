from django import forms
from datetime import date
from dateutil.relativedelta import *
import calendar

class FormCommonUtils():
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
        for i in range(1960, (date.today().year - 17)):
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
        birthday_year = birthday_dictionary.get("birthday_year")
        birthday_month = birthday_dictionary.get("birthday_month")
        birthday_day = birthday_dictionary.get("birthday_day")

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

class RegisterForm(forms.Form):

    FormCommonUtils_obj = FormCommonUtils();
    DAYS_SELECT_CHOICES = FormCommonUtils_obj.get_days_select_choices()
    MONTHS_SELECT_CHOICES = FormCommonUtils_obj.get_months_select_choices()
    YEARS_SELECT_CHOICES = FormCommonUtils_obj.get_years_select_choices()
    GENDERS_SELECT_CHOICES = FormCommonUtils_obj.get_genders_select_choices()

    first_name = forms.CharField(label='Nome', max_length=20, required=True)
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', required=True, choices=DAYS_SELECT_CHOICES)
    birthday_month = forms.ChoiceField(label='Mese', required=True, choices=MONTHS_SELECT_CHOICES)
    birthday_year = forms.ChoiceField(label='Anno', required=True, choices=YEARS_SELECT_CHOICES)
    gender = forms.ChoiceField(label='Sesso', required=True, choices=GENDERS_SELECT_CHOICES)
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

    def clean(self):

        lista_errori = []
        #cleaned_data = super(RegisterForm, self).clean()
        try:
            cleaned_data = super(RegisterForm, self).clean()
        except ValidationError:
            lista_errori.append("compila tutti i campi")

        birthday_dictionary = {
            "birthday_year" : cleaned_data.get("birthday_year"),
            "birthday_month" : cleaned_data.get("birthday_month"),
            "birthday_day" : cleaned_data.get("birthday_day"),
        }

        #if (!FormCommonUtils_obj.check_if_user_is_adult(birthday_dictionary=birthday_dictionary)):
        if (True):
            # raise an exception if user is not adult
            lista_errori.append("altro errore sconosciuto")

        raise forms.ValidationError([
                    forms.ValidationError(lista_errori.pop(), code='error1'),
                    forms.ValidationError(lista_errori.pop(), code='error2'),
                ])

        return True
