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

    ALREADY_MODEL_CHOICES = (
	('', '-'),
	('yes', 'Si'),
	('no', 'No'),
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
        questions_list += question_obj.get_all_questions_about_survey(survey_code=DS_SURVEYS_CODE_IS_MODEL)
        questions_list += question_obj.get_all_questions_about_survey(survey_code=DS_SURVEYS_CODE_IS_NOT_MODEL)

        for question in questions_list:
            question_label = question_obj.get_label_about_question_code(question_code=question.get("question_code"))
	    if question.get("question_type") == "text":
		self.fields[question.get("question_code")] = forms.CharField(label=question_label.get("question_text_woman"), required=question.get("required"), widget=forms.TextInput(attrs={'placeholder': question_label.get("question_hint_woman"), 'case_1_survey_code': question.get("case_1_survey__survey_code"), 'case_2_survey_code': question.get("case_2_survey__survey_code"), 'survey_code': question.get("survey__survey_code"), 'default_hidden': question.get("default_hidden"), 'question_type': question.get("question_type")}))
	    else:
		self.fields[question.get("question_code")] = forms.ChoiceField(label=question_label.get("question_text_woman"), choices=self.ALREADY_MODEL_CHOICES, required=question.get("required"), widget=forms.TextInput(attrs={'placeholder': question_label.get("question_hint_woman"), 'case_1_survey_code': question.get("case_1_survey__survey_code"), 'case_2_survey_code': question.get("case_2_survey__survey_code"), 'survey_code': question.get("survey__survey_code"), 'default_hidden': question.get("default_hidden"), 'question_type': question.get("question_type")})) 

    def clean(self):
	super(SurveyForm, self).clean_form_custom()
        return True

    def save_form(self):
        answer_obj = Answer();
        logger.debug("elenco di risposte preparate per il salvataggio: " + str(self.form_validated_data))
        logger.debug("id_user: " + str(self.request_data.user.id))
        answer_obj.save_answers_list(id_user=self.request_data.user.id, answers_list=self.form_validated_data)

        return True

    def form_actions(self):
        """Function to create new user and logging into website"""
        self.save_form()

        return True
