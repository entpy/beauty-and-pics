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

        survey_obj = Survey()
        question_obj = Question()

        # retrieve a list of questions about a survey
        questions_list = question_obj.get_survey_questions_dictionary(survey_code='interview')

	# logger.info("[build survey form] all questions dict: " + str(questions_list))
        for question_info in questions_list:
            """
            question_info = [
		{
			'selectable_answers': [{
				'answer_code': u 'user_interview__block1__q1__a5',
				'question__question_code': u 'interview__block1__q1'
				'next_question_block_1__block_code': u 'interview__block1__block800',
				'next_question_block_2__block_code': u 'interview__block1__block900',
				'next_question_block_3__block_code': None,
				'next_question_block_4__block_code': None,
				'next_question_block_5__block_code': None,
			}, {
				'answer_code': u 'user_interview__block1__q1__a4',
				'question__question_code': u 'interview__block1__q1'
				'next_question_block_1__block_code': u 'interview__block1__block600',
				'next_question_block_2__block_code': u 'interview__block1__block700',
				'next_question_block_3__block_code': None,
				'next_question_block_4__block_code': None,
				'next_question_block_5__block_code': None,
			}, {
				'answer_code': u 'user_interview__block1__q1__a3',
				'question__question_code': u 'interview__block1__q1'
				'next_question_block_1__block_code': u 'interview__block1__block400',
				'next_question_block_4__block_code': None,
				'next_question_block_2__block_code': u 'interview__block1__block500',
				'next_question_block_3__block_code': None,
				'next_question_block_5__block_code': None,
			}, {
				'answer_code': u 'interview__block1__q1__a2',
				'question__question_code': u 'interview__block1__q1'
				'next_question_block_1__block_code': u 'interview__block1__block200',
				'next_question_block_2__block_code': u 'interview__block1__block300',
				'next_question_block_3__block_code': None,
				'next_question_block_4__block_code': None,
				'next_question_block_5__block_code': None,
			}, {
				'answer_code': u 'interview__block1__q1__a1',
				'question__question_code': u 'interview__block1__q1'
				'next_question_block_1__block_code': u 'interview__block1__block1',
				'next_question_block_2__block_code': u 'interview__block1__block2',
				'next_question_block_3__block_code': u 'interview__block1__block3',
				'next_question_block_4__block_code': u 'interview__block1__block4',
				'next_question_block_5__block_code': None,
			}],
			'survey__survey_code': u 'interview',
			'question_block__block_code': u 'interview__block1',
			'question_code': u 'interview__block1__q1'
			'block_level_1__block_code': None,
			'block_level_2__block_code': None,
			'block_level_3__block_code': None,
			'block_level_4__block_code': None,
			'block_level_5__block_code': None,
			'question_type': u 'select',
			'question_block__block_level': 1,
			'default_hidden': 0,
			'required': 1,
			'order': 0,
		},...]
            """
            question_code = question_info.get("question_code")
            # logger.info("[build survey form] question_code: " + str(question_code))
            # logger.info("[build survey form] question_info: " + str(question_info))
            question_label = survey_obj.get_element_label(element_code=question_code) # TODO: variabilizzare label

            widget_attrs = {
                # 'placeholder': question_label,
                'current_block_code' : question_info.get("question_block__block_code"),
                'current_block_level' : question_info.get("question_block__block_level"),
                'block_level1' : question_info.get("block_level_1__block_code"),
                'block_level2' : question_info.get("block_level_2__block_code"),
                'block_level3' : question_info.get("block_level_3__block_code"),
                'block_level4' : question_info.get("block_level_4__block_code"),
                'block_level5' : question_info.get("block_level_5__block_code"),
                'default_hidden': question_info.get("default_hidden"),
                'question_type': question_info.get("question_type"),
		'select_choices': [],
            }

	    if question_info.get("question_type") == "text":
                # create text input
		self.fields[question_code] = forms.CharField(
                        label=question_label,
                        required=question_info.get("required"),
                        widget=forms.TextInput(attrs=widget_attrs))
            elif question_info.get("question_type") == "select":
                # create select input with select choices
                if question_info.get('selectable_answers'):
                    answer_choices = [('-', '-'),]
                    widget_attrs['select_choices'] = [{
                        'answer_code' : '-',
                        'answer_label' : '-',
                        'next_question_block_code1' : '',
                        'next_question_block_code2' : '',
                        'next_question_block_code3' : '',
                        'next_question_block_code4' : '',
                        'next_question_block_code5' : '',
                    }]
                    for selectable_answer in question_info.get('selectable_answers'):
			# logger.info("[build survey form] selectable_answers: " + str(selectable_answer))
			# logger.info("[build survey form] answer_code: " + str(selectable_answer.get('answer_code')))
                        # answer_choices = answer_choices + ((selectable_answer.get('answer_code'), 'testo ' + str(selectable_answer.get('answer_code')), selectable_answer.get('answer_code')),)
                        answer_choices.append(
                            (
                                selectable_answer.get('answer_code'),
                                survey_obj.get_element_label(element_code=selectable_answer.get('answer_code')),
                            ),
                        )
                        widget_attrs['select_choices'].append(
                            {
                                'answer_code' : selectable_answer.get('answer_code'),
                                'answer_label' : survey_obj.get_element_label(element_code=selectable_answer.get('answer_code')),
                                'next_question_block_code1' : selectable_answer.get('next_question_block_1__block_code'),
                                'next_question_block_code2' : selectable_answer.get('next_question_block_2__block_code'),
                                'next_question_block_code3' : selectable_answer.get('next_question_block_3__block_code'),
                                'next_question_block_code4' : selectable_answer.get('next_question_block_4__block_code'),
                                'next_question_block_code5' : selectable_answer.get('next_question_block_5__block_code'),
                            }
                        )
		self.fields[question_code] = forms.ChoiceField(
                        label=question_label,
                        choices=answer_choices,
                        required=question_info.get("required"),
                        widget=forms.TextInput(attrs=widget_attrs)) 

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
