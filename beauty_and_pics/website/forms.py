from django import forms
from datetime import date
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

class RegisterForm(forms.Form):

    FormCommonUtils_obj = FormCommonUtils();
    DAYS_SELECT_CHOICES = FormCommonUtils_obj.get_days_select_choices()
    MONTHS_SELECT_CHOICES = FormCommonUtils_obj.get_months_select_choices()
    YEARS_SELECT_CHOICES = FormCommonUtils_obj.get_years_select_choices()
    GENDERS_SELECT_CHOICES = FormCommonUtils_obj.get_genders_select_choices()

    first_name = forms.CharField(label='Nome', max_length=20, required=True)
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', max_length=2, required=True, choices=DAYS_SELECT_CHOICES)
    birthday_month = forms.ChoiceField(label='Mese', max_length=2, required=True, choices=MONTHS_SELECT_CHOICES)
    birthday_year = forms.ChoiceField(label='Anno', max_length=4, required=True, choices=YEARS_SELECT_CHOICES)
    gender = forms.CharField(label='Sesso', max_length=1, required=True, choices=GENDERS_SELECT_CHOICES)
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
