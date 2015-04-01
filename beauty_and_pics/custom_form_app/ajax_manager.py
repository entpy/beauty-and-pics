# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from custom_form_app.forms.base_form_class import *
from custom_form_app.forms.register_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from beauty_and_pics.consts import project_constants
from contest_app.models.votes import Vote
from account_app.models import *
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ajaxManager():

    __json_response = None
    __valid_action_list = ()

    def __init__(self, request=None):
        # list of valid methods
	self.__valid_action_list += ('form_validation',)
	self.__valid_action_list += ('elements_list',)
	self.__valid_action_list += ('perform_voting',)

        # retrieve action to perform
        self.ajax_action = request.POST.get("ajax_action")
        # ajax request (POST data)
        self.request = request

    def check_if_action_is_valid(self):
        """Function to check if an ajax action is valid"""
        return self.ajax_action in self.__valid_action_list

    def check_if_is_post(self):
        """Function to check if a request is performed via POST"""
        return_var = False
        if self.request.method == 'POST':
            return_var = True

        return return_var

    def perform_ajax_action(self):
        """Function to perform ajax action"""
        # check if request method sia POST
        if self.check_if_is_post():
            # check if ajax action is valid
            if self.check_if_action_is_valid():
                # ajax action is valid
                logger.debug("ajax_action: " + str(self.ajax_action))
                code = compile("self." + self.ajax_action + "()", '<string>', 'exec')
                exec(code)
            else:
                # return a JSON error response
                self.set_json_response(json_response=json.dumps('{ "error": True, "msg": :"Invalid action"}'))
                logger.error("ATTENZIONE: ajax action non valida (" + str(self.ajax_action) + ")")
        else:
            # return a JSON error response
            self.set_json_response(json_response=json.dumps('{ "error": True, "msg": :"Please call this page via POST method"}'))
            logger.error("ATTENZIONE: ajax action chiamata senza metodo POST (" + str(self.ajax_action) + ")")

        return True

    def get_json_response(self):
        """Function to retrieve json response"""
        return self.__json_response

    def set_json_response(self, json_response=None):
        """Function to set json response"""
        if json_response:
            self.__json_response = json_response

        return True

    def form_validation(self):
        """Function to validate forms via AJAX"""
        logger.debug("ajax_function: @@form_validation@@")

        form_class = self.request.POST.get("form_class")
        # check if form_class is a valid form class
        FormCommonUtils_obj = FormCommonUtils()
        if FormCommonUtils_obj.check_if_form_class_is_valid(form_class=form_class):
            # create a form instance and populate it with data from the request:
            code = compile("form = " + form_class + "(self.request.POST)", '<string>', 'exec')
            exec(code)
            # setting request data attribute
            form.set_current_request(request=self.request)
            # check if form is valid
            form.is_valid()

            # make a json response
            self.set_json_response(json_response=form.get_validation_json_response())

        return True

    def elements_list(self):
        """Function to retrieve a filtered elements list (users or photo book)"""
        # TODO: restituire la lista filtrata di utenti o di foto
        logger.debug("ajax_function: @@elements_list@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        # catwalker, favorite, photobook
        Account_obj = Account()
        elements_list_type = self.request.POST.get("elements_list_type")
        json_account_element = []

        # catwalker section
        if elements_list_type == "catwalker":
            # TODO: creare funzione per elenco dei filtri nella chiamata AJAX
            filter_list = []
            filtered_elements = Account_obj.get_filtered_accounts_list(filters_list=self.request.POST)

            for account in filtered_elements:
                json_account_element.append({
                        "user_id": account.user.id,
                        "user_email": account.user.email,
                        "image_url": "http://lorempixel.com/150/150/nature",
                        }),

        # TODO favorite section
        # TODO photobook section
        """
        data = {
                'success' : True,
                'elements_list': [
                    {"user_id": 1, "user_email": "email1@mail.com"},
                    {"user_id": 2, "user_email": "email2@mail.com"},
                    {"user_id": 3, "user_email": "email3@mail.com"},
                    {"user_id": 4, "user_email": "email4@mail.com"},
                ]
                }
        """

        data = {'success' : True, 'elements_list_type': elements_list_type, 'elements_list': json_account_element, }
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def perform_voting(self):
        """Function to vote a catwalker"""
        logger.debug("ajax_function: @@perform_voting@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

	# build votation dictionary
        votation_data = {}
        votation_data["id_user"] = self.request.POST.get("id_user")
        votation_data["global_vote_points"] = self.request.POST.get("global_vote_points")
        votation_data["face_vote_points"] = self.request.POST.get("face_vote_points")
        votation_data["look_vote_points"] = self.request.POST.get("look_vote_points")
	error_msg = ""

	try:
	    vote_obj = Vote()
	    vote_obj.perform_votation(votation_data, self.request.POST.get("id_user"), self.request.META["REMOTE_ADDR"])
	except VoteUserIdMissingError:
	    error_msg = "Non è stato possibile eseguire la votazione, sii gentile, contatta l'amministratore."
	except VoteMetricMissingError:
	    error_msg = "Seleziona un valore per ogni metrica."
	except VoteMetricWrongValueError:
	    error_msg = "I valori per ogni metrica devono essere compresi tra 1 e 5."
	except ContestNotActiveError:
	    error_msg = "Non è possibile votare fino a che il contest non sarà aperto."
	except UserAlreadyVotedError:
	    error_msg = "Non puoi votare più volte lo stesso utente nell'arco di 48 ore."
	else:
	    # votation performing seems ok
	    pass

	if error_msg:
	    data = {'error' : True, 'message': error_msg }
	else:
	    data = {'success' : True, 'message': 'Grazie per aver votato!' }

	# build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True
