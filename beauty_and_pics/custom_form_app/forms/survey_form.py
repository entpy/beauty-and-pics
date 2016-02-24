# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
# from account_app.models import *
from django_survey.models import *
from django_survey.settings import *
from website.exceptions import *
import logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class SurveyForm(forms.Form, FormCommonUtils):

    # list of validator for this form
    custom_validation_list = (
        'check_all_fields_valid',
    )

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(SurveyForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(SurveyForm, self)

        # retrieve a list of questions about a survey
        question_obj = Question()
        questions_list = question_obj.get_all_questions_about_survey(survey_code=DS_SURVEYS_CODE_ABOUT_USER)
        questions_list = questions_list.update(question_obj.get_all_questions_about_survey(survey_code=DS_SURVEYS_CODE_IS_MODEL))
        questions_list = questions_list.update(question_obj.get_all_questions_about_survey(survey_code=DS_SURVEYS_CODE_IS_NOT_MODEL))

        for question in questions_list:
            question_info = question_obj.get_question_string_about_code(question_code=question.question_code)
            self.fields[question.question_code] = forms.CharField(label=question_info.get("question_text_woman"), required=question_info.get("required"), widget=forms.TextInput(attrs={'placeholder': question_info.get("question_hint_woman")}))

    def clean(self):
	super(SurveyForm, self).clean_form_custom()
        return True

    def save_form(self):
        return_var = False
        """
        if super(SurveyForm, self).form_can_perform_actions():
            account_obj = Account()
            # building birthday date
            birthday_date = account_obj.create_date(date_dictionary={"day" : self.form_validated_data.get("birthday_day"), "month" : self.form_validated_data.get("birthday_month"), "year" : self.form_validated_data.get("birthday_year")}, get_isoformat=True)
            if (birthday_date):
                self.form_validated_data["birthday_date"] = birthday_date
            # update account info
            account_obj.update_data(save_data=self.form_validated_data, user_obj=self.request_data.user)
            return_var = True
        """

        return return_var

    def form_actions(self):
        """Function to create new user and logging into website"""
        return_var = False
        if self.save_form():
            return_var = True

        return return_var
