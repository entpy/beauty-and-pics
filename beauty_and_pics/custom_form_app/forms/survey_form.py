# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from dateutil.relativedelta import *
from custom_form_app.forms.base_form_class import *
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
        # prelevo le variabili aggiuntive che poi andrò a rimuovere
        # ATTENZIONE: i seguenti parametri non possono essere utilizzati come
        # name dell input
        gender = kwargs.pop("gender", None) # fix per far funzionare la init di default del form
        survey_code = kwargs.pop("survey_code", None) # fix per far funzionare la init di default del form

        # parent forms.Form init
        super(SurveyForm, self).__init__(*args, **kwargs)
        FormCommonUtils.__init__(self)

	# current form instance
        self.validation_form = super(SurveyForm, self)

        survey_obj = Survey()
        question_obj = Question()
        user_answer_obj = UserAnswer()

        # retrieve a list of questions about a survey
        questions_list = question_obj.get_survey_questions_dictionary(survey_code=survey_code)

        # identify user gender (TODO: check)
        if gender == 'man':
            element_type = 'question_text_man'
        else:
            element_type = 'question_text_woman'

	# logger.info("[build survey form] all questions dict: " + str(questions_list))
        for question_info in questions_list:
            question_code = question_info.get("question_code")
            # logger.info("[build survey form] question_code: " + str(question_code))
            # logger.info("[build survey form] question_info: " + str(question_info))
            question_label = survey_obj.get_element_label(element_code=question_code, element_type=element_type)

            widget_attrs = {
                # 'placeholder': question_label, # placeholder disabled at the moment
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
                    answer_choices = [('', '-'),]
                    widget_attrs['select_choices'] = [{
                        'answer_code' : '',
                        'answer_label' : '-',
                        'next_question_block_code1' : '',
                        'next_question_block_code2' : '',
                        'next_question_block_code3' : '',
                        'next_question_block_code4' : '',
                        'next_question_block_code5' : '',
                    }]
                    for selectable_answer in question_info.get('selectable_answers'):
                        # per la validazione
                        answer_choices.append(
                            (
                                selectable_answer.get('answer_code'),
                                survey_obj.get_element_label(element_code=selectable_answer.get('answer_code'), element_type=element_type),
                            ),
                        )
                        # per la visualizzazione nel template html
                        widget_attrs['select_choices'].append(
                            {
                                'answer_code' : selectable_answer.get('answer_code'),
                                'answer_label' : survey_obj.get_element_label(element_code=selectable_answer.get('answer_code'), element_type=element_type),
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

    def save_form(self, survey_code):
        Question_obj = Question()
        UserSurvey_obj = UserSurvey()
        UserAnswer_obj = UserAnswer()

        # 1) Creo un nuovo survey, o setto come non pubblicato e da approvare
        #    un survey già esistente
        user_survey = UserSurvey_obj.init_user_survey(survey_code=survey_code, user_id=self.request_data.user.id)

	# 2) Elimino tutte le precedenti risposte del survey
	UserAnswer_obj.delete_survey_answers_by_user(survey_code=survey_code, user_id=self.request_data.user.id)

        # 3) Salvo le risposte: itero su tutti i question_code del survey code e
        #    per ognuno in self.form_validated_data prelevo la risposta
        questions_code_list = Question_obj.get_code_list_by_survey_code(survey_code=survey_code)
        for question_element in questions_code_list:
            UserAnswer_obj.save_answer(user_survey_obj=user_survey, question_id=question_element.get('question_id'), value=self.form_validated_data.get(question_element.get('question_code')))

        return True

    def form_actions(self, survey_code):
        """Function to save user survey"""
        self.save_form(survey_code=survey_code)

        return True

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
