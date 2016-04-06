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

    def check_survey_code_exists(self, survey_code):
	"""Function to check if a survey code exists"""
        return_var = False
        try:
            self.get_by_survey_code(survey_code=survey_code)
            return_var = True
        except Survey.DoesNotExist:
            # survey code does not exist
            pass

        return return_var

    def _create_defaults(self):
	"""Function to create default questions and survey blocks"""

	Survey_obj = Survey()
	QuestionBlock_obj = QuestionBlock()
	# 1) create surveys
	for survey in DS_SURVEY:
            # if surveys already exists, skip
            try:
                Survey_obj.get_by_survey_code(survey_code=survey.get('survey_code'))
            except Survey.DoesNotExist:
                Survey_obj.survey_code = survey.get('survey_code')
                Survey_obj.save()
            else:
                # surveys already exists, skip to next loop
                # salto anche l'inserimento delle possibili domande
                continue

	    # 2) insert all block code
            for question_info in DS_QUESTIONS_AND_SELECTABLE_ANSWERS.get(survey.get('survey_code')):
		QuestionBlock_obj.create(block_code=question_info.get('question_block'), block_level=question_info.get('block_level'))

            # 3) create question's survey and question_blocks
            for question_info in DS_QUESTIONS_AND_SELECTABLE_ANSWERS.get(survey.get('survey_code')):
                # se non esiste, inserisco il QuestionBlock
                Question_obj = Question()
		try:
		    Question_obj.question_block = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('question_block'))
		except QuestionBlock.DoesNotExist:
		    pass
		try:
		    Question_obj.block_level_1 = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('block_code_level_1'))
		except QuestionBlock.DoesNotExist:
		    pass
		try:
		    Question_obj.block_level_2 = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('block_code_level_2'))
		except QuestionBlock.DoesNotExist:
		    pass
		try:
		    Question_obj.block_level_3 = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('block_code_level_3'))
		except QuestionBlock.DoesNotExist:
		    pass
		try:
		    Question_obj.block_level_4 = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('block_code_level_4'))
		except QuestionBlock.DoesNotExist:
		    pass
		try:
		    Question_obj.block_level_5 = QuestionBlock_obj.get_by_block_code(block_code=question_info.get('block_code_level_5'))
		except QuestionBlock.DoesNotExist:
		    pass
                Question_obj.survey = Survey_obj
		Question_obj.question_code = question_info.get('question_code')
                Question_obj.question_type = question_info.get('question_type')
                Question_obj.required = int(question_info.get('required'))
                Question_obj.order = int(question_info.get('order'))
                Question_obj.default_hidden = int(question_info.get('default_hidden'))
                Question_obj.not_to_show = int(question_info.get('not_to_show', 0))
                Question_obj.save()

                # 4) create question's answers
                for question_answer in question_info.get('answers'):
                    SelectableAnswer_obj = SelectableAnswer()
                    SelectableAnswer_obj.question = Question_obj
                    try:
                        SelectableAnswer_obj.next_question_block_1 = QuestionBlock_obj.get_by_block_code(block_code=question_answer.get('next_question_block_1'))
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_1 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_2 = QuestionBlock_obj.get_by_block_code(block_code=question_answer.get('next_question_block_2'))
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_2 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_3 = QuestionBlock_obj.get_by_block_code(block_code=question_answer.get('next_question_block_3'))
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_3 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_4 = QuestionBlock_obj.get_by_block_code(block_code=question_answer.get('next_question_block_4'))
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_4 retrieved
                        pass
                    try:
                        SelectableAnswer_obj.next_question_block_5 = QuestionBlock_obj.get_by_block_code(block_code=question_answer.get('next_question_block_5'))
                    except QuestionBlock.DoesNotExist:
                        # no next_question_block_5 retrieved
                        pass
                    SelectableAnswer_obj.answer_code = question_answer.get('answer_code')
                    SelectableAnswer_obj.order = question_answer.get('order')
                    SelectableAnswer_obj.save()

	return True

    def get_element_label(self, element_code, element_type=False):
	"""Function to retrieve an element label"""
	return_var = ''
	if element_code and element_type:
	    return_var = DS_QUESTIONS_ANSWERS_LABEL.get(element_code)
	    if return_var:
		return_var = return_var.get(element_type)

	return return_var

class QuestionBlock(models.Model):
    question_block_id = models.AutoField(primary_key=True)
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

    def create(self, block_code, block_level=False):
	"""Function to retrieve or create a question block"""
        return_var = None
	logger.info("""
	    def create():
		block_code=""" + str(block_code) + """
		block_level=""" + str(block_level) + """
	""")
        try:
            return_var = self.get_by_block_code(block_code=block_code)
        except QuestionBlock.DoesNotExist:
            # create new question block
            if block_code and block_level:
                QuestionBlock_obj = QuestionBlock()
                QuestionBlock_obj.block_code = block_code
                QuestionBlock_obj.block_level = block_level
                QuestionBlock_obj.save()
                return_var = QuestionBlock_obj

        return return_var

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey)
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
    not_to_show = models.IntegerField(default=0)

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
		'block_level_1__block_code',
		'block_level_2__block_code',
		'block_level_3__block_code',
		'block_level_4__block_code',
		'block_level_5__block_code',
		'question_type',
		'required',
		'order',
		'default_hidden'
	    ).filter(survey__survey_code=survey_code).order_by('order'))

        return return_var

    def get_code_list_by_survey_code(self, survey_code):
        """"Function to retrieve all questions by survey_code"""
        return_var = None
        if survey_code:
            return_var = list(Question.objects.values('question_id', 'question_code').filter(survey__survey_code=survey_code).order_by('order'))

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
                # prepend dictionary to list
		# return_var.insert(0, question_dict)
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
    order = models.IntegerField(default=0)

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
                'next_question_block_1__block_code',
                'next_question_block_2__block_code',
                'next_question_block_3__block_code',
                'next_question_block_4__block_code',
                'next_question_block_5__block_code',
                'answer_code'
            ).filter(question__survey__survey_code=survey_code).order_by('order'))
	    # logger.info("list_by_survey_code: " + str(return_var))

        return return_var

    def create_selectable_answer_dictionary(self, survey_code):
        """"Function to create a dictionary with selectable answers about survey"""
        return_var = {}
        if survey_code:
            selectable_answers = self.list_by_survey_code(survey_code=survey_code)
            for answer in selectable_answers:
                # logger.info("question_code: " + str(answer.get('question__question_code')))
                # logger.info("answer: " + str(answer))
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
    published = models.IntegerField(default=DS_CONST_NOT_PUBLISHED, null=True, blank=True) # 0 not published, 1 published
    status = models.IntegerField(default=DS_CONST_MUST_BE_APPROVED, null=True, blank=True) # 3 da approvare, 2 in fase di approvazione, 1 approvato, 0 non approvato

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.user_survey_id)

    def set_survey_as_not_approved(self, survey_code, user_id):
        """Function to set an existing survey as not published and da approvare"""
        return_var = False
        try:
            UserSurvey_obj = UserSurvey.objects.get(survey__survey_code=survey_code, user__id=user_id)
        except UserSurvey.DoesNotExist:
            raise
        else:
            UserSurvey_obj.published = DS_CONST_NOT_PUBLISHED
            UserSurvey_obj.status = DS_CONST_MUST_BE_APPROVED
            UserSurvey_obj.save()
            return_var = UserSurvey_obj

        return return_var

    def get_user_survey_by_id(self, user_survey_id):
        """Function to retrieve user survey by user_survey_id"""
        return_var = None
        try:
            return_var = UserSurvey.objects.get(user_survey_id=user_survey_id)
        except UserSurvey.DoesNotExist:
            raise

        return return_var

    def get_user_survey(self, survey_code, user_id):
        """Function to retrieve user survey"""
        return_var = None
        try:
            return_var = UserSurvey.objects.get(survey__survey_code=survey_code, user__id=user_id)
        except UserSurvey.DoesNotExist:
            raise

        return return_var

    def is_survey_approved(self):
        """Function to test if a survey object was approved"""
        return_var = False
        if self.status == DS_CONST_APPROVED:
            return_var = True

        return return_var

    def set_approving_status(self, approving_status):
        """Function to set approving status to an user survey"""
        return_var = False
        self.status = approving_status
        self.save()
        return_var = True

        return return_var

    def set_publishing_status(self, publishing_status):
        """Function to set publishing status to an user survey"""
        return_var = False
        self.published = publishing_status
        self.save()
        return_var = True

        return return_var

    def set_pending_approving_status(self):
        """Function to set approving status to pending"""
        return_var = False
	self.status = DS_CONST_PENDING_APPROVAL
	self.check_message = None
	self.save()
	return_var = True

        return return_var

    def mark_as_approved(self):
        """Function to mark survey as not approved"""
        return_var = False
	self.status = DS_CONST_APPROVED
	self.check_message = None
	self.save()
	return_var = True

        return return_var

    def mark_as_not_approved(self, check_message):
        """Function to mark survey as not approved"""
        return_var = False
	self.status = DS_CONST_NOT_APPROVED
	self.check_message = check_message
	self.save()
	return_var = True

        return return_var

    def get_survey_approving_label(self, approving_status):
        """Function to retrieve approving status label related with approving_status"""
        return_var = False

        if approving_status == DS_CONST_MUST_BE_APPROVED:
            return_var = 'Da approvare'
        elif approving_status == DS_CONST_PENDING_APPROVAL:
            return_var = 'Approvazione in corso'
        elif approving_status == DS_CONST_APPROVED:
            return_var = 'Approvata'
        elif approving_status == DS_CONST_NOT_APPROVED:
            return_var = 'Non approvata'

        return return_var

    def get_survey_publishing_label(self, publishing_status):
        """Function to retrieve publishing status label related with approving_status"""
        return_var = False

        if publishing_status == DS_CONST_NOT_PUBLISHED:
            return_var = 'Non pubblicata'
        elif publishing_status == DS_CONST_PUBLISHED:
            return_var = 'Pubblicata'

        return return_var

    def create_new_user_survey(self, survey_code, user_id):
        """Function to create an user survey (not published and da approvare) by survey_code and user_id"""
        Survey_obj = Survey()
        UserSurvey_obj = UserSurvey()
        UserSurvey_obj.user_id = user_id
        UserSurvey_obj.survey = Survey_obj.get_by_survey_code(survey_code=survey_code)
        UserSurvey_obj.published = DS_CONST_NOT_PUBLISHED
        UserSurvey_obj.status = DS_CONST_MUST_BE_APPROVED
        UserSurvey_obj.save()

        return UserSurvey_obj

    def init_user_survey(self, survey_code, user_id):
        """Function to init a new or existing survey"""
        return_var = False
        try:
            return_var = self.set_survey_as_not_approved(survey_code=survey_code, user_id=user_id)
        except UserSurvey.DoesNotExist:
            return_var = self.create_new_user_survey(survey_code=survey_code, user_id=user_id)

        return return_var

class UserAnswer(models.Model):
    user_answer_id = models.AutoField(primary_key=True)
    user_survey = models.ForeignKey(UserSurvey)
    question = models.ForeignKey(Question)
    value = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.user_answer_id)

    def save_answer(self, user_survey_obj, question_id, value):
        """Function to save a single question answer"""
        return_var = False

        if user_survey_obj and question_id and value:
            UserAnswer_obj = UserAnswer()
            UserAnswer_obj.question_id = question_id
            UserAnswer_obj.user_survey = user_survey_obj
            UserAnswer_obj.value = value
            UserAnswer_obj.save()
            return_var = UserAnswer_obj

        return return_var

    def delete_survey_answers_by_user(self, survey_code, user_id):
	"""Function to delete all answers about survey_code and user_id"""
	UserAnswer.objects.filter(user_survey__survey__survey_code=survey_code, user_survey__user__id=user_id).delete()

        return True

    def get_survey_answers_form_by_user_id(self, survey_code, user_id):
        """
            Function to retrieve all question codes and related answer values by survey_code and user_id
            survey_answer_list = {
                'question_code1' : 'value1',
                'question_code2' : 'value2',
                'question_code3' : 'value3',
                ...
            }
        """
	return_var = {}
        question_answer_list = list(UserAnswer.objects.values('question__question_code', 'value').filter(user_survey__survey__survey_code=survey_code, user_survey__user__id=user_id, value__isnull=False).order_by('question__order'))
	for single_question_answer in question_answer_list:
	    return_var[single_question_answer.get('question__question_code')] = single_question_answer.get('value')
	return return_var

    def get_survey_answers_by_user_id(self, survey_code, user_id, gender=None, only_if_published=False):
        """
            Function to retrieve all question_codes, question_labels and related answer_values by survey_code and user_id
        """
        return_var = []
	if only_if_published:
	    question_answer_list = list(UserAnswer.objects.values('question__question_code', 'question__question_type', 'value').filter(user_survey__survey__survey_code=survey_code, user_survey__user__id=user_id, user_survey__published=DS_CONST_PUBLISHED, question__not_to_show=False, value__isnull=False).order_by('question__order'))
	else:
	    question_answer_list = list(UserAnswer.objects.values('question__question_code', 'question__question_type', 'value').filter(user_survey__survey__survey_code=survey_code, user_survey__user__id=user_id, question__not_to_show=False,value__isnull=False).order_by('question__order'))

        if gender == 'man':
            element_type = 'question_text_man'
        else:
            element_type = 'question_text_woman'

        if question_answer_list:
            for single_question_answer in question_answer_list:
                question_label = DS_QUESTIONS_ANSWERS_LABEL.get(single_question_answer.get('question__question_code'))
                if single_question_answer.get('question__question_type') == 'select':
                    # la risposta della select è in DS_QUESTIONS_ANSWERS_LABEL
                    answer_label = DS_QUESTIONS_ANSWERS_LABEL.get(single_question_answer.get('value'))
                    return_var.append({'label': question_label.get(element_type), 'value': answer_label.get(element_type)})
                else:
                    # la risposta della select è direttamente in value di single_question_answer
                    return_var.append({'label': question_label.get(element_type), 'value': single_question_answer.get('value')})

        return return_var
