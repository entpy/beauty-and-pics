from django import forms
import calendar

class FormCommonUtils():
    def get_days_select_value(self):
            """Get a list of days for select"""
            return range(1, 32)

    def get_months_select_value(self):
            """Get a list of months for select"""
            months_choices = []
            for i in range(1,13):
                    months_choices.append((i, calendar.month_name[i]))
            return months_choices

    def get_years_select_value(self):
            """Get a list of years for select"""
            # TODO: (current year - 18)
            #                    |
            #                    V
            return range(1950, 1999)

class RegisterForm(forms.Form):

    first_name = forms.CharField(label='Nome', max_length=20, required=True)
    last_name = forms.CharField(label='Cognome', max_length=20, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', required=True)
    birthday_month = forms.ChoiceField(label='Mese', required=True)
    birthday_year = forms.ChoiceField(label='Anno', required=True)
    gender = forms.CharField(label='Sesso', max_length=1, required=True)
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
