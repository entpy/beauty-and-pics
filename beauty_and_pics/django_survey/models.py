# -*- coding: utf-8 -*-

from django.db import models, connection
from django.contrib.auth.models import User
from .settings import *
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

"""
class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_code = models.CharField(max_length=50)
    survey_description = models.CharField(max_length=150)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.survey_id)

    def _manage_surveys(self):
        ""Function to create survey and related questions""
        question_obj = Question()

        self._create_default_surveys()
        question_obj._create_default_questions()

        return True

    def _create_default_surveys(self):
        ""Function to create default surveys""
        # 3 survey, uno comune, uno se modella, uno se non modella

        if DS_SURVEYS_LIST:
            for survey in DS_SURVEYS_LIST:
                if not self.get_survey_by_code(survey_code=survey.get("survey_code")):
                    # survey must be saved
                    survey_obj = Survey()
                    survey_obj.survey_code = survey.get("survey_code")
                    survey_obj.survey_description = survey.get("survey_description")
                    survey_obj.save()

        return True

    def get_survey_by_code(self, survey_code):
        ""Function to retrieve survey by code""
        return_var = None
        try:
            return_var = Survey.objects.get(survey_code=survey_code)
        except Survey.DoesNotExist:
            pass

        return return_var

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey)
    question_code = models.CharField(max_length=50)
    question_type = models.CharField(max_length=20)
    required = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    default_hidden = models.IntegerField(default=0)
    case_1_survey = models.ForeignKey(Survey, null=True, blank=True, related_name='case_1_survey')
    case_2_survey = models.ForeignKey(Survey, null=True, blank=True, related_name='case_2_survey')

    class Meta:
        app_label = 'django_survey'
	unique_together = ('survey', 'question_code')

    def __unicode__(self):
        return str(self.question_id)

    def _create_default_questions(self):
        ""Function to create default questions""
        question_obj = Question()
        survey_obj = Survey()

        if DS_SURVEYS_QUESTIONS:
            for question in DS_SURVEYS_QUESTIONS:
                try:
		    self.get_question_by_code(question_code=question.get('question_code'))
		except:
		    logger.info("inserisco default questions: " + str(question.get('question_code')))
                    # question must be saved
                    question_obj = Question()
                    question_obj.survey = survey_obj.get_survey_by_code(survey_code=question.get('survey_code'))
                    question_obj.question_code = question.get('question_code')
                    question_obj.question_type = question.get('question_type')
                    question_obj.required = question.get('required')
                    question_obj.order = question.get('order')
                    question_obj.default_hidden = question.get('default_hidden')
                    question_obj.case_1_survey = survey_obj.get_survey_by_code(survey_code=question.get('case_1_survey_code'))
                    question_obj.case_2_survey = survey_obj.get_survey_by_code(survey_code=question.get('case_2_survey_code'))
                    question_obj.save()

        return True

    def get_question_by_code(self, question_code):
        ""Function to retrieve question by code""
        return_var = None
        try:
            return_var = Question.objects.get(question_code=question_code)
        except Question.DoesNotExist:
            raise

        return return_var

    def get_all_questions_about_survey(self, survey_code_list):
        ""Function to retrieve all questions about a survey code list""

        return list(Question.objects.values('required', 'question_code', 'question_id', 'question_type', 'order', 'default_hidden', 'survey__survey_code', 'survey__survey_id', 'case_1_survey__survey_code', 'case_2_survey__survey_code').filter(survey__survey_code__in=survey_code_list).order_by("order"))

    def get_all_questions(self):
        ""Function to retrieve all questions""

        return list(Question.objects.all().order_by("order"))

    def get_label_about_question_code(self, question_code):
        ""Function to retrieve strings a question""
        return_var = {}

        if question_code:
            return_var["question_text_woman"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_text_woman")
            return_var["question_text_man"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_text_man")
            return_var["question_hint_woman"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_hint_woman")
            return_var["question_hint_man"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_hint_man")

        return return_var

class Answer(models.Model):
    id_answer = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)
    answer_text = models.CharField(max_length=500, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_survey'
	unique_together = ('question', 'survey', 'user')

    def __unicode__(self):
        return str(self.id_answer)

    def save_answers_list(self, id_user, answers_list, survey_code_list):
        ""Function to save an answers list about user""
        question_obj = Question()
        survey_obj = Survey()
        questions_list = question_obj.get_all_questions_about_survey(survey_code_list=survey_code_list)

        logger.debug("elenco di risposte: " + str(answers_list))

        if id_user and answers_list and questions_list:
            # TODO: iterare solo sulle domande di determinati survey
            for question in questions_list:
		# save user answer
		# TODO
		if answers_list[question.get('question_code')]:
		    self.save_answers(answer_text=answers_list[question.get('question_code')], question_id=question.get('question_id'), survey_id=question.get('survey__survey_id'), id_user=id_user)

        return True

    def save_answers(self, answer_text, question_id, survey_id, id_user):
        ""Function to save/edit a single question's answers about user""
        answer_obj = Answer()

        try:
            # check if answer already exists
            # controllare, se esiste carica quella esistente, altrimenti no
            answer_obj = self.get_question_survey_answer(survey_id=survey_id, question_id=question_id)
        except Answer.DoesNotExist:
            pass

        logger.info("salvataggio risposta, answer_text: " + str(answer_text) + " question_id: " + str(question_id) + " survey_id: " + str(survey_id) + " id_user: " + str(id_user))

        answer_obj.question_id = question_id
        answer_obj.survey_id = survey_id
        answer_obj.user_id = id_user
        answer_obj.answer_text = answer_text
        answer_obj.save()

        return True

    def get_question_survey_answer(self, survey_id, question_id):
        ""Function to retrieve an answer about survey and question""
        return_var = False

        try:
            return_var = Answer.objects.get(survey__survey_id=survey_id, question__question_id=question_id)
        except Answer.DoesNotExist:
            raise

        return return_var

    def get_answers_about_survey_list(self, survey_list):
        ""Function to retrieve answers about a survey list""
        return_var = {}
	answers_list =  list(Answer.objects.values('question__question_code', 'question__question_type', 'question__case_1_survey', 'question__case_2_survey', 'answer_text').filter(survey__survey_code__in=survey_list))
	if answers_list:
	     for single_answer_info in answers_list:
		return_var[single_answer_info.get('question__question_code')] = single_answer_info.get('answer_text')
		return_var[single_answer_info.get('question__question_code')]['question_type'] = single_answer_info.get('question__question_type')
		return_var[single_answer_info.get('question__question_code')]['case_1_survey'] = single_answer_info.get('question__case_1_survey')
		return_var[single_answer_info.get('question__question_code')]['case_2_survey'] = single_answer_info.get('question__case_2_survey')

	logger.info("all answers about survey: " + str(return_var))

        return return_var
"""

class QuestionGroup(models.Model):
    question_group_id = models.AutoField(primary_key=True)
    group_code = models.CharField(max_length=150)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.question_group_id)

    def get_by_group_code(self, group_code):
	"""Function to retrieve a group by group_code"""
        return_var = None
        try:
            return_var = QuestionGroup.objects.get(group_code=group_code)
        except QuestionGroup.DoesNotExist:
            raise

        return return_var

class QuestionBlock(models.Model):
    question_block_id = models.AutoField(primary_key=True)
    question_group = models.ForeignKey(QuestionGroup)
    block_code = models.CharField(max_length=200)
    block_level = models.IntegerField(default=0)
    block_code_level_0 = models.ForeignKey('self', related_name='block_code_level0', null=True, blank=True) # | -
    block_code_level_1 = models.ForeignKey('self', related_name='block_code_level1', null=True, blank=True) # |  depth level
    block_code_level_2 = models.ForeignKey('self', related_name='block_code_level2', null=True, blank=True) # |
    block_code_level_3 = models.ForeignKey('self', related_name='block_code_level3', null=True, blank=True) # |
    block_code_level_4 = models.ForeignKey('self', related_name='block_code_level4', null=True, blank=True) # V +
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.question_block_id)

    def get_by_block_code(self, block_code):
	"""Function to retrieve a question block by block_code"""
        return_var = None
        try:
            return_var = QuestionBlock.objects.get(block_code=block_code)
        except QuestionBlock.DoesNotExist:
            raise

        return return_var

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_block = models.ForeignKey(QuestionBlock)
    question_code = models.CharField(max_length=150)
    question_type = models.CharField(max_length=100)
    required = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    default_hidden = models.IntegerField(default=0)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.question_id)

    def get_by_question_group_code(self, question_group_code):
        """"Function to retrieve all questions about question_group_code"""
        return_var = None
        if question_group_code:
            return_var = list(Question.objects.values('question_block__block_code',
							'question_block__question_group__group_code',
							'question_block__block_level',
							'question_block__block_code_level_0__block_code',
							'question_block__block_code_level_1__block_code',
							'question_block__block_code_level_2__block_code',
							'question_block__block_code_level_3__block_code',
							'question_block__block_code_level_4__block_code',
							'question_code',
							'question_type',
							'required',
							'order',
							'default_hidden'
						    ).filter(
							question_block__question_group__group_code=question_group_code
						    ).order_by('order'))

        return return_var

    def get_survey_questions_dictionary(self, question_group_code):
        """"Function to build survey questions dictionary about question_group_code"""
        SelectableAnswer_obj = SelectableAnswer()
        return_var = []

        if question_group_code:
            # list of all selectable answers about question_group_code
            selectable_answers_list = SelectableAnswer_obj.create_selectable_answer_dictionary(question_group_code=question_group_code)
            # list of all questions about question_group_code
            questions_list = self.get_by_question_group_code(question_group_code=question_group_code)
	    # logger.info("[get_by_question_group_code] question_list: " + str(questions_list))
            for question in questions_list:
                # question info
                # logger.info("[get_by_question_group_code] question: " + str(question))
                question_dict = {}
		if question_dict:
		    question_dict = question_dict.extends(question)
		else:
		    question_dict = question
                # question answer(s)
                question_dict['selectable_answers'] = selectable_answers_list.get(question.get('question_code'))
                # append dictionary to list
                return_var.append(question_dict)
        # logger.info("[get_by_question_group_code] question_list: " + str(return_var))

        return return_var

class SelectableAnswer(models.Model):
    selectable_answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question)
    next_question_block = models.ForeignKey(QuestionBlock, null=True, blank=True)
    answer_code = models.CharField(max_length=150)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.selectable_answer_id)

    def list_by_question_group_code(self, question_group_code):
        """"Function to retrieve all selectable answers about question_group_code"""
        return_var = None
        if question_group_code:
            return_var = list(SelectableAnswer.objects.values('question__question_code', 'next_question_block__block_code', 'answer_code').filter(question__question_block__question_group__group_code=question_group_code))
	    # logger.info("list_by_question_group_code: " + str(return_var))

        return return_var

    def create_selectable_answer_dictionary(self, question_group_code):
        """"Function to create a dictionary with selectable answers about question"""
        return_var = {}
        if question_group_code:
            selectable_answers = self.list_by_question_group_code(question_group_code=question_group_code)
            for answer in selectable_answers:
                # logger.info("question_code: " + str(answer.get('question__question_code')))
                logger.info("answer: " + str(answer))
                if not return_var.get(answer.get('question__question_code')):
                    return_var[answer.get('question__question_code')] = []
		return_var[answer.get('question__question_code')].append(answer)

	# logger.info("[create_selectable_answer_dictionary]: " + str(return_var))

        return return_var

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    question_group = models.ForeignKey(QuestionGroup)
    user = models.ForeignKey(User)
    survey_code = models.CharField(max_length=150) # interview, user_report, ...
    creation_date = models.DateTimeField(auto_now_add=True)
    check_required = models.IntegerField(null=True, blank=True)
    check_message = models.CharField(max_length=500, null=True, blank=True) # message after survey check (e.g not approved because...)
    status = models.IntegerField(null=True, blank=True) # 2 da approvare, 1 approvato, 0 non approvato

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.survey_id)

    def _create_defaults(self):
	"""Function to create default questions and survey blocks"""

	# 1) create question groups
	for question_group in DS_QUESTIONS_GROUPS:
            # if question_group already exists skip
	    QuestionGroup_obj = QuestionGroup()
            try:
                QuestionGroup_obj.get_by_group_code(group_code=question_group)
            except QuestionGroup.DoesNotExist:
                QuestionGroup_obj.group_code = question_group
                QuestionGroup_obj.save()
            else:
                # question group already exists, skip to next loop
                continue

	    # 2) create question block
            QuestionBlockLevel_obj = QuestionBlock()
	    for question_block in DS_QUESTIONS_BLOCK:
		QuestionBlock_obj = QuestionBlock()
		QuestionBlock_obj.question_group = QuestionGroup_obj
		QuestionBlock_obj.block_code = question_block.get('block_code')
		QuestionBlock_obj.block_level = question_block.get('block_level')
                if question_block.get('block_code_level_0'):
                    QuestionBlock_obj.block_code_level_0 = QuestionBlockLevel_obj.get_by_block_code(block_code=question_block.get('block_code_level_0'))
                if question_block.get('block_code_level_1'):
                    QuestionBlock_obj.block_code_level_1 = QuestionBlockLevel_obj.get_by_block_code(block_code=question_block.get('block_code_level_1'))
                if question_block.get('block_code_level_2'):
                    QuestionBlock_obj.block_code_level_2 = QuestionBlockLevel_obj.get_by_block_code(block_code=question_block.get('block_code_level_2'))
                if question_block.get('block_code_level_3'):
                    QuestionBlock_obj.block_code_level_3 = QuestionBlockLevel_obj.get_by_block_code(block_code=question_block.get('block_code_level_3'))
                if question_block.get('block_code_level_4'):
                    QuestionBlock_obj.block_code_level_4 = QuestionBlockLevel_obj.get_by_block_code(block_code=question_block.get('block_code_level_4'))
		QuestionBlock_obj.order = question_block.get('order')
		QuestionBlock_obj.save()

            # 3) create questions
            for question_info in DS_QUESTIONS_AND_SELECTABLE_ANSWERS:
                QuestionBlock_obj = QuestionBlock()
                Question_obj = Question()
                Question_obj.question_block = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('question_block'))
                Question_obj.question_code = question_info.get('question_code')
                Question_obj.question_type = question_info.get('question_type')
                Question_obj.required = int(question_info.get('required'))
                Question_obj.order = int(question_info.get('order'))
                Question_obj.default_hidden = int(question_info.get('default_hidden'))
                Question_obj.save()

                # 4) create question's answers
                for question_answer in question_info.get('answers'):
                    QuestionBlockNext_obj = QuestionBlock()
                    SelectableAnswer_obj = SelectableAnswer()
                    SelectableAnswer_obj.question = Question_obj
                    try:
                        SelectableAnswer_obj.next_question_block = QuestionBlockNext_obj.get_by_block_code(block_code=question_answer.get('next_question_block'))
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block retrieved
                        pass
                    else:
                        SelectableAnswer_obj.answer_code = question_answer.get('answer_code')
                        SelectableAnswer_obj.save()

	return True

class UserAnswer(models.Model):
    user_answer_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey)
    selectable_answer = models.ForeignKey(SelectableAnswer)
    text = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.user_answer_id)
