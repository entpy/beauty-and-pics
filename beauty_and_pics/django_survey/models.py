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
    id_survey = models.AutoField(primary_key=True)
    survey_code = models.CharField(max_length=50)
    survey_description = models.CharField(max_length=150)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.id_survey)

    def _manage_surveys(self):
        """Function to create survey and related questions"""
        question_obj = Question()

        self._create_default_surveys()
        question_obj._create_default_questions()

        return True

    def _create_default_surveys(self):
        """Function to create default surveys"""
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
        """Function to retrieve survey by code"""
        return_var = None
        try:
            return_var = Survey.objects.get(survey_code=survey_code)
        except Survey.DoesNotExist:
            pass

        return return_var

class Question(models.Model):
    id_question = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey)
    question_code = models.CharField(max_length=50)
    question_type = models.CharField(max_length=20)
    required = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.id_question)

    def _create_default_questions(self):
        """Function to create default questions"""
        question_obj = Question()
        survey_obj = Survey()

        if DS_SURVEYS_QUESTIONS:
            for question in DS_SURVEYS_QUESTIONS:
                if not self.get_question_by_code(question_code=question.get('question_code')):
                    # question must be saved
                    question_obj = Question()
                    question_obj.survey = survey_obj.get_survey_by_code(survey_code=question.get('survey_code'))
                    question_obj.question_code = question.get('question_code')
                    question_obj.question_type = question.get('question_type')
                    question_obj.required = question.get('required')
                    question_obj.order = question.get('order')
                    question_obj.save()

        return True

    def get_question_by_code(self, question_code):
        """Function to retrieve question by code"""
        return_var = None
        try:
            return_var = Question.objects.get(question_code=question_code)
        except Question.DoesNotExist:
            pass

        return return_var

    def get_all_questions_about_survey(self, survey_code):
        """Function to retrieve all questions about a survey"""

        return list(Question.objects.filter(survey__survey_code=survey_code).order_by("order"))

    def get_question_string_about_code(self, question_code):
        """Function to retrieve strings a question"""
        return_var = {}

        if question_code:
            question = self.get_question_by_code(question_code=question_code)
            return_var["question_text_woman"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_text_woman")
            return_var["question_text_man"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_text_man")
            return_var["question_hint_woman"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_hint_woman")
            return_var["question_hint_man"] = DS_SURVEYS_QUESTIONS_LABEL.get(question_code).get("question_hint_man")
            return_var["required"] = question.required
            return_var["question_code"] = question.question_code
            return_var["question_type"] = question.question_type
            return_var["order"] = question.order
            return_var["survey_code"] = question.survey.survey_code

        return return_var

class Answer(models.Model):
    id_answer = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)
    answer_text = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        app_label = 'django_survey'

    def __unicode__(self):
        return str(self.id_answer)

"""
    question = models.CharField(max_length=500)
    gender = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)
    birthday_date = models.DateField(null=True)
    hair = models.CharField(max_length=15, null=True, blank=True)
    eyes = models.CharField(max_length=15, null=True, blank=True)
    height = models.CharField(max_length=4, null=True, blank=True)
    newsletters_bitmask = models.CharField(max_length=20, default=(project_constants.WEEKLY_REPORT_EMAIL_BITMASK + project_constants.CONTEST_REPORT_EMAIL_BITMASK), null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    can_be_shown = models.IntegerField(default=0) # indica se l'utente può essere mostrato nella passerella
    prize_status = models.IntegerField(default=project_constants.PRIZE_CANNOT_BE_REDEEMED, null=True, blank=True) # 0 l'utente NON può richiedere il premio, 1 l'utente può richiedere il premio, 2 l'utente ha già richiesto il premio
    # activation via email
    activation_key = models.CharField(max_length=40, blank=True)
"""
