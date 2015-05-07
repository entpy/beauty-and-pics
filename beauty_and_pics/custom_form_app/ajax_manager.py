# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from custom_form_app.forms.base_form_class import *
from custom_form_app.forms.register_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from beauty_and_pics.consts import project_constants
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

    def __init__(self, request=None):
        # list of valid methods
        self.__valid_action_list += ('form_validation',)
        self.__valid_action_list += ('elements_list',)
        self.__valid_action_list += ('perform_voting',)
        self.__valid_action_list += ('save_image',)
        self.__valid_action_list += ('delete_image',)
        self.__valid_action_list += ('add_favorite',)

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
            Book_obj = Book()

            for user_info in filtered_elements:
                logger.debug("element list: " + str(user_info))
                json_account_element.append({
                        "user_id": user_info["user__id"],
                        "user_email": user_info["user__email"],
                        "total_points": user_info.get("total_points"),
                        "thumbnail_image_url": Book_obj.get_profile_thumbnail_image_url(user_id=user_info["user__id"]),
                }),

        # photobook section
        if elements_list_type == "photobook":
            Book_obj = Book()
            user_id = self.request.POST.get("user_id")
            filtered_elements = Book_obj.get_photobook_list(user_id=user_id, filters_list=self.request.POST)

            for image in filtered_elements:
                logger.debug("element list: " + str(image))
                json_account_element.append({
                        "image_id": image["image_id__id"],
                        "thumbnail_image_url": settings.MEDIA_URL + image["image_id__thumbnail_image__image"],
                        "image_url": settings.MEDIA_URL + image["image_id__image"],
                }),

        # TODO favorite section
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
        votation_data["user_id"] = self.request.POST.get("user_id")
        votation_data["global_vote_points"] = self.request.POST.get("global_vote_points")
        votation_data["smile_vote_points"] = self.request.POST.get("smile_vote_points")
        votation_data["look_vote_points"] = self.request.POST.get("look_vote_points")
        error_msg = ""

        try:
            vote_obj = Vote()
            vote_obj.perform_votation(votation_data, self.request.POST.get("user_id"), self.request.META["REMOTE_ADDR"])
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
            data = {'success' : True, 'message': "Grazie per aver votato. Tieni d'occhio la classifica!" }

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
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(croppedImageDoesNotExistError.get_error_code) + "), sii gentile contatta l'amministratore!" }
        except imageTypeWrongError:
            logger.error("Image type inserito non valido: " + str(self.request) + " | error code: " + str(imageTypeWrongError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(imageTypeWrongError.get_error_code) + "), sii gentile contatta l'amministratore!" }
        else:
            data = {'success' : True, 'image_url': saved_image_url, 'image_id': saved_image_id, 'message': "immagine salvata correttamente!" }

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
        data = {'error' : True, 'message': "Controllare i parametri della chiamata" }
        image_id = self.request.POST.get("image_id")
        user_id = self.request.user.id

        try:
            image_delete_status = book_obj.delete_book_image(image_id=image_id, user_id=user_id)
        except bookImageDoesNotExistError:
            logger.error("Errore nell'eliminazione dell'immagine, l'immagine richiesta non esiste nella tabella Book: " + str(self.request) + " | error code: " + str(bookImageDoesNotExistError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(bookImageDoesNotExistError.get_error_code) + "), sii gentile contatta l'amministratore!" }
        except croppedImageDoesNotExistError:
            logger.error("Errore nell'eliminazione dell'immagine, l'immagine richiesta non esiste nella tabella cropUploadedImages: " + str(self.request) + " | error code: " + str(croppedImageDoesNotExistError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(croppedImageDoesNotExistError.get_error_code) + "), sii gentile contatta l'amministratore!" }
        except deleteImageReferenceError:
            logger.error("Errore nell'eliminazione dell'immagine, gli id utenti non coincidono: " + str(self.request) + " | error code: " + str(deleteImageReferenceError.get_error_code))
            data = {'error' : True, 'message': "Errore inaspettato (codice=" + str(deleteImageReferenceError.get_error_code) + "), sii gentile contatta l'amministratore!" }
        else:
            if image_delete_status:
                data = {'success' : True, 'image_id': image_id, 'message': "Immagine eliminata correttamente!" }

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def add_favorite(self):
        """Function to add a favorite"""
        logger.debug("ajax_function: @@add_favorite@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        account_obj = Account()
        data = {'error' : True, 'message': "Controllare i parametri della chiamata" }
        favorite_user_id = self.request.POST.get("user_id")
        user_id = self.request.user.id

        # add favorite
        favorite_obj = Favorite()
        try:
            add_favorite_status = favorite_obj.add_favorite(user_id=user_id, favorite_user_id=favorite_user_id)
        except userAlreadyAddedToFavoritesError:
            data = {'error' : True, 'type': "already_added" }
        else:
            if add_favorite_status:
                data = {'success' : True }

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True
