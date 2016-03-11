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
        questions_list = question_obj.get_survey_questions_dictionary(question_group_code='user_interview')

	# logger.info("[build survey form] all questions dict: " + str(questions_list))
        for question_info in questions_list:
            """
            question_info = {
                    'question_block__block_code': u 'user_interview__user_identify',
                    'question_block__path_code': u 'path001',
                    'selectable_answers': [{
                            'answer_code': u 'user_interview__user_identify__q1__model_pro',
                            'next_question_block__block_code': u 'user_interview__model_pro',
                            'question__question_code': u 'user_interview__user_identify__q1'
                    }, {
                            'answer_code': u 'user_interview__user_identify__q1__model_beginner',
                            'next_question_block__block_code': u 'user_interview__model_beginner',
                            'question__question_code': u 'user_interview__user_identify__q1'
                    }, {
                            'answer_code': u 'user_interview__user_identify__q1__photo_passionate',
                            'next_question_block__block_code': u 'user_interview__photo_passionate',
                            'question__question_code': u 'user_interview__user_identify__q1'
                    }, {
                            'answer_code': u 'user_interview__user_identify__q1__fashion_passionate',
                            'next_question_block__block_code': u 'user_interview__fashion_passionate',
                            'question__question_code': u 'user_interview__user_identify__q1'
                    }, {
                            'answer_code': u 'user_interview__user_identify__q1__just_for_fun',
                            'next_question_block__block_code': u 'user_interview__just_for_fun',
                            'question__question_code': u 'user_interview__user_identify__q1'
                    }],
                    'required': 1 L,
                    'question_code': u 'user_interview__user_identify__q1',
                    'default_hidden': 0 L,
                    'question_type': u 'select',
                    'question_block__question_group__group_code': u 'user_interview',
                    'order': 0 L
            }
            """
            question_code = question_info.get("question_code")
            # logger.info("[build survey form] question_code: " + str(question_code))
            # logger.info("[build survey form] question_info: " + str(question_info))
            question_label = question_code # TODO: variabilizzare label
	    if question_info.get("question_type") == "text":
                # create text input
		self.fields[question_code] = forms.CharField(label=question_label, required=question_info.get("required"), widget=forms.TextInput(attrs={'placeholder': question_label, 'question_block' : question_info.get("question_block__block_code"), 'default_hidden': question_info.get("default_hidden"), 'question_type': question_info.get("question_type"), 'path_code': question_info.get("question_block__path_code"), 'child_path_code': question_info.get("question_block__child_path_code")}))
            elif question_info.get("question_type") == "select":
                # create select input with select choices
                if question_info.get('selectable_answers'):
                    answer_choices = [{
                        'answer_code' : '-',
                        'answer_label' : '-',
                        'next_question_block_code' : '',
                    }]
                    for selectable_answer in question_info.get('selectable_answers'):
			logger.info("[build survey form] selectable_answers: " + str(selectable_answer))
			logger.info("[build survey form] answer_code: " + str(selectable_answer.get('answer_code')))
                        # answer_choices = answer_choices + ((selectable_answer.get('answer_code'), 'testo ' + str(selectable_answer.get('answer_code')), selectable_answer.get('answer_code')),)
                        answer_choices.append(
                            {
                                'answer_code' : selectable_answer.get('answer_code'),
                                'answer_label' : 'testo ' + str(selectable_answer.get('answer_code')),
                                'next_question_block_code' : selectable_answer.get('next_question_block__block_code'),
                            }
                        )
		self.fields[question_code] = forms.ChoiceField(label=question_label, choices=answer_choices, required=question_info.get("required"), widget=forms.TextInput(attrs={'placeholder': question_label, 'choices_dict' : '', 'question_block' : question_info.get("question_block__block_code"), 'default_hidden': question_info.get("default_hidden"), 'question_type': question_info.get("question_type"), 'path_code': question_info.get("question_block__path_code"), 'child_path_code': question_info.get("question_block__child_path_code")})) 

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
