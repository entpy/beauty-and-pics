# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from custom_form_app.forms.base_form_class import *
from custom_form_app.forms.register_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from custom_form_app.forms.help_request_form import *
from custom_form_app.forms.report_user_form import *
from custom_form_app.forms.unsubscribe_form import *
from beauty_and_pics.consts import project_constants
from beauty_and_pics.common_utils import CommonUtils
from contest_app.models.votes import Vote
from account_app.models import *
from contest_app.models import Contest
from upload_image_box.models import cropUploadedImages
from website.exceptions import *
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ajaxManager():

    __json_response = None
    __valid_action_list = ()
    cookie_key = ""
    cookie_value = ""
    cookie_expiring = ""

    def __init__(self, request=None):
        # list of valid methods
        self.__valid_action_list += ('form_validation',)
        self.__valid_action_list += ('elements_list',)
        self.__valid_action_list += ('perform_voting',)
        self.__valid_action_list += ('save_image',)
        self.__valid_action_list += ('delete_image',)
        self.__valid_action_list += ('add_favorite',)
        self.__valid_action_list += ('get_user_info',)

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

    def attach_cookie_to_response(self, response):
        """Function to attach a cookie to response"""
        return_var = None
        if response and self.cookie_key:
            # cookie with expiring in time from next votation
            response.set_cookie(key=self.cookie_key, value=self.cookie_value, max_age=self.cookie_expiring)
            return_var = response

        return response

    def perform_ajax_action(self):
        """Function to perform ajax action"""
        # check if request method is POST
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

	    # build JSON response
	    json_data_string = form.get_validation_json_response()
	else:
	    logger.debug("no----" + form_class)
            data = { 'error' : True, 'message': 'Form class does not exist', }
	    json_data_string = json.dumps(data)

	# make a json response
	self.set_json_response(json_response=json_data_string)

        return True

    def elements_list(self):
        """Function to retrieve a filtered elements list (users or photo book)"""
        logger.debug("ajax_function: @@elements_list@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        # catwalker, favorite, photobook
        Account_obj = Account()
        elements_list_type = self.request.POST.get("elements_list_type")
        json_account_element = []

        # catwalker section
        if elements_list_type == "catwalker":
            # retrieve current contest_type
            contest_obj = Contest()
            filtered_elements = Account_obj.get_filtered_accounts_list(filters_list=self.request.POST, contest_type=contest_obj.get_contest_type_from_session(request=self.request))
            book_obj = Book()

            for user_info in filtered_elements:
                logger.debug("element list: " + str(user_info))
                json_account_element.append({
                        "user_id": user_info["user__id"],
                        "user_email": user_info["user__email"],
                        "total_points": user_info.get("total_points"),
                        "thumbnail_image_url": book_obj.get_profile_thumbnail_image_url(user_id=user_info["user__id"]),
                }),

        # photobook section
        if elements_list_type == "photobook":
            book_obj = Book()
            user_id = self.request.POST.get("user_id")
            filtered_elements = book_obj.get_photobook_list(user_id=user_id, filters_list=self.request.POST)

            for image in filtered_elements:
                logger.debug("element list: " + str(image))
                json_account_element.append({
                        "image_id": image["image_id__id"],
                        "thumbnail_image_url": settings.MEDIA_URL + image["image_id__thumbnail_image__image"],
                        "image_url": settings.MEDIA_URL + image["image_id__image"],
                }),

        # favorite section
        if elements_list_type == "favorite":
            book_obj = Book()
            favorite_obj = Favorite()
            user_id = self.request.user.id
            filtered_elements = favorite_obj.get_favorites_list(user_id=user_id, filters_list=self.request.POST)

            for favorite_user in filtered_elements:
                logger.debug("element list: " + str(favorite_user))
                json_account_element.append({
                        "user_id": favorite_user["favorite_user__id"],
                        "thumbnail_image_url": book_obj.get_profile_thumbnail_image_url(user_id=favorite_user["favorite_user__id"]),
                }),
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

        data = {'success' : True, 'elements_list_type': elements_list_type, 'elements_list': json_account_element,}
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def perform_voting(self):
        """Function to vote a catwalker"""
        logger.debug("ajax_function: @@perform_voting@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        # common method class init
        CommonUtils_obj = CommonUtils()

        # build votation dictionary
        votation_data = {}
        votation_data["user_id"] = self.request.POST.get("user_id")
        votation_data["global_vote_points"] = self.request.POST.get("global_vote_points")
        votation_data["smile_vote_points"] = self.request.POST.get("smile_vote_points")
        votation_data["look_vote_points"] = self.request.POST.get("look_vote_points")
        error_msg = ""

        try:
            vote_obj = Vote()
            vote_obj.perform_votation(votation_data, self.request.POST.get("user_id"), CommonUtils_obj.get_ip_address(request=self.request), request=self.request)
        except VoteUserIdMissingError:
            error_msg = "Non è stato possibile eseguire la votazione, sii gentile, contatta l'amministratore."
        except VoteMetricMissingError:
            error_msg = "Seleziona un valore per ogni metrica."
        except VoteMetricWrongValueError:
            error_msg = "I valori per ogni metrica devono essere compresi tra 1 e 5."
        except ContestNotActiveError:
            error_msg = "Non è possibile votare fino all'apertura del concorso."
        except UserAlreadyVotedError:
            error_msg = "Non puoi votare più volte lo stesso utente nell'arco di 7 giorni."
        else:
            # votation performing seems ok, attach cookie to response
            self.cookie_key = project_constants.USER_ALREADY_VOTED_COOKIE_NAME + str(self.request.POST.get("user_id"))
            self.cookie_value = True
            self.cookie_expiring = project_constants.SECONDS_BETWEEN_VOTATION
            pass

        if error_msg:
            data = {'error' : True, 'message': error_msg}
        else:
            data = {'success' : True, 'message': "Grazie per aver votato. Tieni d'occhio la classifica!"}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def save_image(self):
        """Function to save a new image"""
        logger.debug("ajax_function: @@save_image@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        book_obj = Book()

        # retrieve uploaded image data
        image_data = {}
        image_data["image_id"] = self.request.POST.get("image_id")
        image_data["image_type"] = self.request.POST.get("image_type")
        image_data["user"] = self.request.user

        # TODO: proseguire con i controlli (forse, è tardi per pensarci)
        try:
            saved_image_obj = book_obj.save_book_image(image_data=image_data)
            saved_image_url = saved_image_obj.image_id.image.url
            saved_image_id = saved_image_obj.image_id.id
        except croppedImageDoesNotExistError:
            logger.error("Errore nell'upload dell'immagine profilo, l'immagine richiesta non esiste nella tabella cropUploadedImages: " + str(self.request) + " | error code: " + str(croppedImageDoesNotExistError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(croppedImageDoesNotExistError.get_error_code) + "), sii gentile contatta l'amministratore!"}
        except imageTypeWrongError:
            logger.error("Image type inserito non valido: " + str(self.request) + " | error code: " + str(imageTypeWrongError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(imageTypeWrongError.get_error_code) + "), sii gentile contatta l'amministratore!"}
        else:
            data = {'success' : True, 'image_url': saved_image_url, 'image_id': saved_image_id, 'message': "immagine salvata correttamente!"}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def delete_image(self):
        """Function to delete an image"""
        logger.debug("ajax_function: @@delete_image@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        book_obj = Book()

        # retrieve uploaded image data
        data = {'error' : True, 'message': "Controllare i parametri della chiamata"}
        image_id = self.request.POST.get("image_id")
        user_id = self.request.user.id

        try:
            image_delete_status = book_obj.delete_book_image(image_id=image_id, user_id=user_id)
        except bookImageDoesNotExistError:
            logger.error("Errore nell'eliminazione dell'immagine, l'immagine richiesta non esiste nella tabella Book: " + str(self.request) + " | error code: " + str(bookImageDoesNotExistError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(bookImageDoesNotExistError.get_error_code) + "), sii gentile contatta l'amministratore!"}
        except croppedImageDoesNotExistError:
            logger.error("Errore nell'eliminazione dell'immagine, l'immagine richiesta non esiste nella tabella cropUploadedImages: " + str(self.request) + " | error code: " + str(croppedImageDoesNotExistError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(croppedImageDoesNotExistError.get_error_code) + "), sii gentile contatta l'amministratore!"}
        except deleteImageReferenceError:
            logger.error("Errore nell'eliminazione dell'immagine, gli id utenti non coincidono: " + str(self.request) + " | error code: " + str(deleteImageReferenceError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(deleteImageReferenceError.get_error_code) + "), sii gentile contatta l'amministratore!"}
        else:
            if image_delete_status:
                data = {'success' : True, 'image_id': image_id, 'message': "Immagine eliminata correttamente!"}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def add_favorite(self):
        """Function to add a favorite"""
        logger.debug("ajax_function: @@add_favorite@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        account_obj = Account()
        data = {'error' : True, 'message': "Controllare i parametri della chiamata"}
        favorite_user_id = self.request.POST.get("user_id")
        user_id = self.request.user.id

        # add favorite
        favorite_obj = Favorite()
        try:
            add_favorite_status = favorite_obj.add_favorite(user_id=user_id, favorite_user_id=favorite_user_id)
        except userAlreadyAddedToFavoritesError:
            data = {'error' : True, 'type': "already_added"}
        else:
            if add_favorite_status:
                data = {'success' : True}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def get_user_info(self):
        """Function to retrieve user info"""
        logger.debug("ajax_function: @@get_user_info@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        account_obj = Account()
        book_obj = Book()
        data = {'error' : True, 'message': "Controllare i parametri della chiamata"}
        user_id = self.request.POST.get("user_id")

        # retrieve user info
        try:
            account_info = account_obj.custom_user_id_data(user_id=user_id)
        except Account.DoesNotExist:
            # user id doesn't exists
            pass
        else:
            # retrieve contest user info
            contest_account_info = account_obj.get_contest_account_info(user_id=user_id)
            # retrieve profile image url
            profile_image_url = book_obj.get_profile_image_url(user_id=user_id)
            # response data
            response_data = {
                "user_id" : account_info["user_id"],
                "user_first_name" : account_info["first_name"],
                "user_last_name" : account_info["last_name"],
                "user_ranking" : contest_account_info["ranking"],
                "user_points" : contest_account_info["total_points"],
                "user_profile_image_url" : profile_image_url,
            }
            data = {'success' : True, "user_info" : response_data}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True
