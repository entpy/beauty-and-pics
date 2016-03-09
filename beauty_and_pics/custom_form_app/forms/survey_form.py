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

    """
    ALREADY_MODEL_CHOICES = (
	('-', '-'),
	('yes', 'Si'),
	('no', 'No'),
    )
    """

    def __init__(self, *args, **kwargs):
        # parent forms.Form init
        super(SurveyForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(SurveyForm, self)

        # retrieve a list of questions about a survey
        question_obj = Question()
        questions_list = question_obj.get_by_question_group_code(question_group_code='user_interview')

	# logger.info("[build survey form] all questions dict: " + str(questions_list))
        for question_code, question_info in questions_list.iteritems():
            # logger.info("[build survey form] question_code: " + str(question_code))
            # logger.info("[build survey form] question_info: " + str(question_info))
            question_label = question_code # TODO: variabilizzare label
	    if question_info.get("question_type") == "text":
                # create text input
		self.fields[question_code] = forms.CharField(label=question_label, required=question_info.get("required"), widget=forms.TextInput(attrs={'placeholder': question_label, 'question_block' : question_info.get("question_block__block_code"), 'default_hidden': question_info.get("default_hidden"), 'question_type': question_info.get("question_type")}))
            elif question_info.get("question_type") == "select":
                # create select input with select choices
                if question_info.get('selectable_answers'):
                    answer_choices = (('-', '-'),)
                    for selectable_answer in question_info.get('selectable_answers'):
			logger.info("[build survey form] selectable_answers: " + str(selectable_answer))
			logger.info("[build survey form] answer_code: " + str(selectable_answer.get('answer_code')))
                        answer_choices = answer_choices + ((selectable_answer.get('answer_code'), 'testo ' + str(selectable_answer.get('answer_code'))),)
		self.fields[question_code] = forms.ChoiceField(label=question_label, choices=answer_choices, required=question_info.get("required"), widget=forms.TextInput(attrs={'placeholder': question_label, 'question_block' : question_info.get("question_block__block_code"), 'default_hidden': question_info.get("default_hidden"), 'question_type': question_info.get("question_type")})) 

    def clean(self):
	super(SurveyForm, self).clean_form_custom()
        return True

    def save_form(self):
        """
        answer_obj = Answer();
        logger.debug("elenco di risposte preparate per il salvataggio: " + str(self.form_validated_data))
        logger.debug("id_user: " + str(self.request_data.user.id))
        answer_obj.save_answers_list(id_user=self.request_data.user.id, answers_list=self.form_validated_data, survey_code_list=[DS_SURVEYS_CODE_ABOUT_USER, DS_SURVEYS_CODE_IS_MODEL, DS_SURVEYS_CODE_IS_NOT_MODEL])
        """

        return True

    def form_actions(self):
        """Function to create new user and logging into website"""
        self.save_form()

        return True
