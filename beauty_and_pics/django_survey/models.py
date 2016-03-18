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

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_code = models.CharField(max_length=150)
    validation_required = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.survey_id)

    def get_by_survey_code(self, survey_code):
	"""Function to retrieve a survey by survey_code"""
        return_var = None
        try:
            return_var = Survey.objects.get(survey_code=survey_code)
        except Survey.DoesNotExist:
            raise

        return return_var

    def _create_defaults(self):
	"""Function to create default questions and survey blocks"""

	Survey_obj = Survey()
	QuestionBlock_obj = QuestionBlock()
	# 1) create surveys
	for survey_code in DS_SURVEY:
            # if surveys already exists, skip
            try:
                Survey_obj.get_by_survey_code(survey_code=survey_code)
            except Survey.DoesNotExist:
                Survey_obj.survey_code = survey_code
                Survey_obj.save()
            else:
                # surveys already exists, skip to next loop
                # salto anche l'inserimento delle possibili domande
                continue

            # 2) create question's survey and question_blocks
            for question_info in DS_QUESTIONS_AND_SELECTABLE_ANSWERS.get(survey_code):
                # se non esiste, inserisco il QuestionBlock
                Question_obj = Question()
                Question_obj.survey = Survey_obj
                # create or retrieve question_block
                Question_obj.question_block = QuestionBlock_obj.get_or_create(block_code=question_info.get('question_block'), survey_id=Survey_obj.survey_id, block_level=question_info.get('block_level'))
                Question_obj.question_code = question_info.get('question_code')
                Question_obj.block_level_1 = QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_1'))
                Question_obj.block_level_2 = QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_2'))
                Question_obj.block_level_3 = QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_3'))
                Question_obj.block_level_4 = QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_4'))
                Question_obj.block_level_5 = QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_5'))
                Question_obj.question_type = question_info.get('question_type')
                Question_obj.required = int(question_info.get('required'))
                Question_obj.order = int(question_info.get('order'))
                Question_obj.default_hidden = int(question_info.get('default_hidden'))
                Question_obj.save()
		logger.info("""
		    insert question:
			survey=""" + str(Survey_obj) + """
			question_block=""" + str(QuestionBlock_obj.get_or_create(block_code=question_info.get('question_block'), survey_id=Survey_obj.survey_id, block_level=question_info.get('block_level'))) + """
			question_code=""" + str(question_info.get('question_code')) + """
			block_level_1=""" + str(QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_1'))) + """
			block_level_2=""" + str(QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_2'))) + """
			block_level_3=""" + str(QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_3'))) + """
			block_level_4=""" + str(QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_4'))) + """
			block_level_5=""" + str(QuestionBlock_obj.get_or_create(block_code=question_info.get('block_code_level_5'))) + """
			question_type=""" + str(question_info.get('question_type')) + """
			required=""" + str(question_info.get('required')) + """
			order=""" + str(question_info.get('order')) + """
			default_hidden=""" + str(question_info.get('default_hidden')) + """
		""")

                # 3) create question's answers
                for question_answer in question_info.get('answers'):
                    SelectableAnswer_obj = SelectableAnswer()
                    SelectableAnswer_obj.question = Question_obj
                    try:
                        SelectableAnswer_obj.next_question_block_1 = QuestionBlock_obj.get_or_create(block_code=question_answer.get('next_question_block_1'), survey_id=Survey_obj.survey_id, block_level=1)
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_1 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_2 = QuestionBlock_obj.get_or_create(block_code=question_answer.get('next_question_block_2'), survey_id=Survey_obj.survey_id, block_level=2)
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_2 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_3 = QuestionBlock_obj.get_or_create(block_code=question_answer.get('next_question_block_3'), survey_id=Survey_obj.survey_id, block_level=3)
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_3 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_4 = QuestionBlock_obj.get_or_create(block_code=question_answer.get('next_question_block_4'), survey_id=Survey_obj.survey_id, block_level=4)
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_4 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_5 = QuestionBlock_obj.get_or_create(block_code=question_answer.get('next_question_block_5'), survey_id=Survey_obj.survey_id, block_level=5)
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_5 retrieved
                        pass
                    SelectableAnswer_obj.answer_code = question_answer.get('answer_code')
                    SelectableAnswer_obj.save()

	return True

class QuestionBlock(models.Model):
    question_block_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey)
    block_code = models.CharField(max_length=200)
    block_level = models.IntegerField()

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

    def get_or_create(self, block_code, survey_id=False, block_level=False):
	"""Function to retrieve or create a question block"""
        return_var = None
	logger.info("""
	    def get_or_create():
		block_code=""" + str(block_code) + """
		survey_id=""" + str(survey_id) + """
		block_level=""" + str(block_level) + """
	""")
        try:
            return_var = self.get_by_block_code(block_code=block_code)
        except QuestionBlock.DoesNotExist:
            # create new question block
            if survey_id and block_code and block_level:
                QuestionBlock_obj = QuestionBlock()
                QuestionBlock_obj.survey_id = survey_id
                QuestionBlock_obj.block_code = block_code
                QuestionBlock_obj.block_level = block_level
                QuestionBlock_obj.save()
                return_var = QuestionBlock_obj

        return return_var

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_block = models.ForeignKey(QuestionBlock)
    question_code = models.CharField(max_length=200)
    block_level_1 = models.ForeignKey(QuestionBlock, related_name='block_level1', null=True, blank=True)
    block_level_2 = models.ForeignKey(QuestionBlock, related_name='block_level2', null=True, blank=True)
    block_level_3 = models.ForeignKey(QuestionBlock, related_name='block_level3', null=True, blank=True)
    block_level_4 = models.ForeignKey(QuestionBlock, related_name='block_level4', null=True, blank=True)
    block_level_5 = models.ForeignKey(QuestionBlock, related_name='block_level5', null=True, blank=True)
    question_type = models.CharField(max_length=100)
    required = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    default_hidden = models.IntegerField(default=0)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.question_id)

    def get_by_survey_code(self, survey_code):
        """"Function to retrieve all questions by survey_code"""
        return_var = None
        if survey_code:
            return_var = list(Question.objects.values(
                'question_block__block_code',
		'question_code',
		'survey__survey_code',
		'question_block__block_level',
		'block_level1__block_code',
		'block_level2__block_code',
		'block_level3__block_code',
		'block_level4__block_code',
		'block_level5__block_code',
		'question_type',
		'required',
		'order',
		'default_hidden'
	    ).filter(survey__survey_code=survey_code).order_by('order'))

        return return_var

    def get_survey_questions_dictionary(self, survey_code):
        """"Function to build survey questions dictionary about survey_code"""
        SelectableAnswer_obj = SelectableAnswer()
        return_var = []

        if survey_code:
            # list of all selectable answers about survey_code
            selectable_answers_list = SelectableAnswer_obj.create_selectable_answer_dictionary(survey_code=survey_code)
            # list of all questions about question_group_code
            questions_list = self.get_by_survey_code(survey_code=survey_code)
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
    next_question_block_1 = models.ForeignKey(QuestionBlock, related_name='next_question_block1', null=True, blank=True)
    next_question_block_2 = models.ForeignKey(QuestionBlock, related_name='next_question_block2', null=True, blank=True)
    next_question_block_3 = models.ForeignKey(QuestionBlock, related_name='next_question_block3', null=True, blank=True)
    next_question_block_4 = models.ForeignKey(QuestionBlock, related_name='next_question_block4', null=True, blank=True)
    next_question_block_5 = models.ForeignKey(QuestionBlock, related_name='next_question_block5', null=True, blank=True)
    answer_code = models.CharField(max_length=200)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.selectable_answer_id)

    def list_by_survey_code(self, survey_code):
        """"Function to retrieve all selectable answers about survey"""
        return_var = None
        if survey_code:
            return_var = list(SelectableAnswer.objects.values(
                'question__question_code',
                'next_question_block1__question_block',
                'next_question_block2__question_block',
                'next_question_block3__question_block',
                'next_question_block4__question_block',
                'next_question_block5__question_block',
                'answer_code'
            ).filter(question__survey__survey_code=survey_code))
	    # logger.info("list_by_survey_code: " + str(return_var))

        return return_var

    def create_selectable_answer_dictionary(self, survey_code):
        """"Function to create a dictionary with selectable answers about survey"""
        return_var = {}
        if survey_code:
            selectable_answers = self.list_by_survey_code(survey_code=survey_code)
            for answer in selectable_answers:
                # logger.info("question_code: " + str(answer.get('question__question_code')))
                logger.info("answer: " + str(answer))
                if not return_var.get(answer.get('question__question_code')):
                    return_var[answer.get('question__question_code')] = []
		return_var[answer.get('question__question_code')].append(answer)

	# logger.info("[create_selectable_answer_dictionary]: " + str(return_var))

        return return_var

class UserSurvey(models.Model):
    user_survey_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    survey = models.ForeignKey(Survey)
    creation_date = models.DateTimeField(auto_now_add=True)
    check_message = models.CharField(max_length=500, null=True, blank=True) # message after survey check (e.g not approved because...)
    status = models.IntegerField(null=True, blank=True) # 2 da approvare, 1 approvato, 0 non approvato

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.user_survey_id)

class UserAnswer(models.Model):
    user_answer_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey)
    selectable_answer = models.ForeignKey(SelectableAnswer)
    text = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.user_answer_id)
