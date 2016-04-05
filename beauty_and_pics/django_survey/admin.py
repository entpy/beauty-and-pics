# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django_survey.models import UserAnswer, UserSurvey
from django_survey.settings import DS_CONST_NOT_PUBLISHED, DS_CONST_PUBLISHED
from account_app.models.accounts import Account
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class SurveyAdmin(admin.ModelAdmin):
    pass

# admin custom view {{{
# require AdminPlus -> https://github.com/jsocol/django-adminplus
# TODO: check che funzioni
def verify_user_survey(request, *args, **kwargs):
    """View to approve or disapprove a user survey (admin side)"""

    user_survey_obj = UserSurvey()
    user_answer_obj = UserAnswer()
    account_obj = Account()

    try:
        # dal kwargs['user_survey_id'] tiro fuori le informazioni dell'utente e tutte le risposte
        existing_user_survey_obj = user_survey_obj.get_user_survey_by_id(user_survey_id=kwargs['user_survey_id'])
    except UserSurvey.DoesNotExist:
        raise

    if request.method == 'POST' and int(request.POST.get('verify_survey_form_sent')):
        # controllo se abilitare o no l'intervista
        if int(request.POST.get('approved')) == 1:
            # set survey as approved
            existing_user_survey_obj.mark_as_approved()
            # publish survey on user profile
            existing_user_survey_obj.set_publishing_status(publishing_status=DS_CONST_PUBLISHED)
            # set message
            messages.add_message(request, messages.SUCCESS, 'Il survey è stato approvato e pubblicato correttamente')
        else:
            # ops...survey cannot be validated
            existing_user_survey_obj.mark_as_not_approved(request.POST.get('not_approved_text'))
            # set survey as NOT published
            existing_user_survey_obj.set_publishing_status(publishing_status=DS_CONST_NOT_PUBLISHED)
            messages.add_message(request, messages.SUCCESS, 'Il survey NON è stato approvato')

        # XXX facoltativo: scegliere se mandare o no una mail di notifica all'utente

        # redirect
        return HttpResponseRedirect('/admin/verify-interview/' + str(kwargs['user_survey_id']) + '/')

    # user_id
    user_id = existing_user_survey_obj.user.id
    # account info
    account_info = account_obj.custom_user_id_data(user_id=user_id)
    # get user survey questions and answers (per mostrare la preview sel survey)
    user_questions_answers = user_answer_obj.get_survey_answers_by_user_id(survey_code=existing_user_survey_obj.survey.survey_code, user_id=user_id, gender=account_info.get("gender"))
    # retrieve survey publishing status label and approving status label
    publishing_status_label = user_survey_obj.get_survey_publishing_label(publishing_status=existing_user_survey_obj.published)
    approving_status_label = user_survey_obj.get_survey_approving_label(approving_status=existing_user_survey_obj.status)

    context = {
            'title': 'Approvazione intervista',
            'app_name': 'django_survey',
            'user_first_name' : account_info.get("first_name"),
            'user_last_name' : account_info.get("last_name"),
            'user_email' : account_info.get("email"),
            'user_gender' : account_info.get("gender"),
            "profile_url": settings.SITE_URL + "/passerella/dettaglio-utente/" + str(user_id) + "/",
            'adminform': False,
            'user_questions_answers': user_questions_answers,
            'user_survey_id': kwargs['user_survey_id'] or '',
	    'publishing_status_label': publishing_status_label,
	    'approving_status_label': approving_status_label,
    }

    return render(request, 'admin/verify-interview.html', context)
# admin custom view }}}

admin.site.register(UserSurvey, SurveyAdmin)
admin.site.register_view('verify-interview/(?P<user_survey_id>\d+)/?', 'Verify user survey', view=verify_user_survey)
