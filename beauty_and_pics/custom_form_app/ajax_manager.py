# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import formats
from django.contrib.auth.models import User
from custom_form_app.forms.base_form_class import *
from custom_form_app.forms.register_form import *
from custom_form_app.forms.password_recover import *
from custom_form_app.forms.account_edit_form import *
from custom_form_app.forms.area51_form import *
from custom_form_app.forms.help_request_form import *
from custom_form_app.forms.report_user_form import *
from custom_form_app.forms.unsubscribe_form import *
from custom_form_app.forms.get_prize_form import GetPrizeForm
from custom_form_app.forms.fast_register_form import FastRegisterForm
from custom_form_app.forms.survey_form import SurveyForm
from beauty_and_pics.consts import project_constants
from beauty_and_pics.common_utils import CommonUtils
from contest_app.models.votes import Vote
from account_app.models import *
from contest_app.models import Contest
from upload_image_box.models import cropUploadedImages
from notify_system_app.models import Notify
from django_survey.models import UserSurvey, Survey
from django_survey.settings import DS_CONST_NOT_PUBLISHED, DS_CONST_PUBLISHED, DS_CONST_PENDING_APPROVAL, DS_CONST_APPROVED
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
        self.__valid_action_list += ('count_unread_notify',)
        self.__valid_action_list += ('add_photoboard_like',)
        self.__valid_action_list += ('resend_confirmation_email',)
        self.__valid_action_list += ('publish_interview',)
        self.__valid_action_list += ('unpublish_interview',)
        self.__valid_action_list += ('add_image_to_photocontest',)
        self.__valid_action_list += ('remove_photocontest_image',)
        self.__valid_action_list += ('add_photocontest_image_like',)

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

    def return_valid_filtered_list(self, filtered_list, show_limit):
        """Restituisco la lista filtrata in base al numero di elementi rimasti da caricare"""
        show_limit = int(show_limit)
        return_var = []
        if self.check_if_exists_more_elements(filtered_list=filtered_list, show_limit=show_limit):
            # se esistono ancora elementi da caricare mi fermo al penultimo
            # elemento nella lista -> limite = -1. Es ci sono 7 elementi in db
            # ma ne ho richesti 5 (e quindi filtered_list ne contiene 5+1)
            return_var = filtered_list[:-1]
        else:
            # se la lista NON è vuota
            if filtered_list:
                # se non esistono ulteriori elementi da caricare prelevo tutti gli
                # elementi rimanenti nella lista, quindi sono al di sotto del
                # limite di visualizzazione. Es. ci sono 3 elementi in db ma ne ho
                # chiesti 5
                return_var = filtered_list

        return return_var

    def check_if_exists_more_elements(self, filtered_list, show_limit):
        """
        Controllo se esistono ancora possibili elementi da caricare
        "filtered_list" è la lista con n+1 elementi, se contiene più
        elementi del limite imposto, allora esistono ulteriori elementi
        caricabili (Es. elementi_filtrati 6, limite visualizzazione 5,
        6 > 5 quindi esistono ulteriori elementi).
        """
        show_limit = int(show_limit)
        exists_more_elements = False
        # check if exists elements (can be an enpty list)
        if filtered_list:
            if len(filtered_list) > int(show_limit-1):
                # esistono ulteriori elementi da caricare (quindi mostro il pulsante "load more")
                exists_more_elements = True

        return exists_more_elements

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
            if self.request.POST.get('extra_param1', None):
                if self.request.POST.get('extra_param2', None):
                    # init con 2 parametri aggiuntivi
                    code = compile("form = " + form_class + "(self.request.POST, extra_param1=self.request.POST.get('extra_param1'), extra_param2=self.request.POST.get('extra_param2'))", '<string>', 'exec')
                else:
                    # init con 1 parametro aggiuntivo
                    code = compile("form = " + form_class + "(self.request.POST, extra_param1=self.request.POST.get('extra_param1'))", '<string>', 'exec')
            else:
                # init senza parametri aggiuntivi
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
        """Function to retrieve a filtered elements list (catwalker, favorite, photobook or notify)"""
        logger.debug("ajax_function: @@elements_list@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))
        from django_photo_contest.models import PhotoContestPictures

        account_obj = Account()
        filters_list = self.request.POST.copy()
        json_account_element = []
	show_load_button = False
        elements_list_type = filters_list.get("elements_list_type")
        filters_list["show_limit"] = int(filters_list["show_limit"]) + 1 # trick to hide "load more" button
        filters_list["elements_per_call"] = int(filters_list["elements_per_call"]) + 1 # trick to hide "load more" button

        # catwalker section
        if elements_list_type == "catwalker":
            # retrieve current contest_type
            contest_obj = Contest()
            book_obj = Book()

            # tiro fuori filtered_list + 1 e la controllo con filtered_list,
            # se c'e' un elemento in più non nascondo il pulsante, altrimenti lo nascondo
            filtered_list = account_obj.get_filtered_accounts_list(filters_list=filters_list, contest_type=contest_obj.get_contest_type_from_session(request=self.request))
            # return a valid filtered list, trick to hide "load more" button
            valid_filtered_list = self.return_valid_filtered_list(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"])

            for user_info in valid_filtered_list:
                logger.debug("element list: " + str(user_info))
                json_account_element.append({
                        "user_id": user_info["user__id"],
                        "user_first_name": user_info["user__first_name"],
                        "user_last_name": user_info["user__last_name"],
                        "user_email": user_info["user__email"],
                        "total_points": user_info.get("total_points"),
                        "thumbnail_image_url": book_obj.get_profile_thumbnail_image_url(user_id=user_info["user__id"]),
                }),

        # photobook section
        if elements_list_type == "photobook":
            book_obj = Book()
            user_id = filters_list.get("user_id")

            # tiro fuori filtered_list + 1 e la controllo con filtered_list,
            # se ce un elemento in più non nascondo il pulsante, altrimenti lo nascondo
            filtered_list = book_obj.get_photobook_list(user_id=user_id, filters_list=filters_list)
            # return a valid filtered list, trick to hide "load more" button
            valid_filtered_list = self.return_valid_filtered_list(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"])

            for image in valid_filtered_list:
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

            # tiro fuori filtered_list + 1 e la controllo con filtered_list,
            # se ce un elemento in più non nascondo il pulsante, altrimenti lo nascondo
            filtered_list = favorite_obj.get_favorites_list(user_id=user_id, filters_list=filters_list)
            # return a valid filtered list, trick to hide "load more" button
            valid_filtered_list = self.return_valid_filtered_list(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"])

            for favorite_user in valid_filtered_list:
                logger.debug("element list: " + str(favorite_user))
                json_account_element.append({
                        "user_id": favorite_user["favorite_user__id"],
                        "thumbnail_image_url": book_obj.get_profile_thumbnail_image_url(user_id=favorite_user["favorite_user__id"]),
                }),

        # last upload section
        if elements_list_type == "last_upload":
            book_obj = Book()
	    contest_obj = Contest()

            # tiro fuori filtered_list + 1 e la controllo con filtered_list,
            # se ce un elemento in più non nascondo il pulsante, altrimenti lo nascondo
            filtered_list = book_obj.get_all_photobook_list(contest_type=contest_obj.get_contest_type_from_session(request=self.request), filters_list=filters_list)
            # return a valid filtered list, trick to hide "load more" button
            valid_filtered_list = self.return_valid_filtered_list(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"])

            for photobook_element in valid_filtered_list:
                logger.debug("element list: " + str(photobook_element))
		thumbnail_url = book_obj.get_image_url(book_image_id=photobook_element["image_id__thumbnail_image"])
		if thumbnail_url:
		    json_account_element.append({
			    "user_id": photobook_element["user__id"],
			    "thumbnail_image_url": book_obj.get_base_image_url() + thumbnail_url,
		    }),

        # photocontest section
        if elements_list_type == "photocontest":
            photo_contest_pictures_obj = PhotoContestPictures()
	    contest_obj = Contest()

            # tiro fuori filtered_list + 1 e la controllo con filtered_list,
            # se ce un elemento in più non nascondo il pulsante, altrimenti lo nascondo
            photo_contest_code = filters_list.get("photo_contest_code")
            filtered_list = photo_contest_pictures_obj.get_photocontest_images(photo_contest_code=photo_contest_code, contest_type_code=contest_obj.get_contest_type_from_session(request=self.request), filters_list=filters_list)
            # return a valid filtered list, trick to hide "load more" button
            valid_filtered_list = self.return_valid_filtered_list(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"])

            for single_element in valid_filtered_list:
                logger.debug("element list: " + str(single_element))
		json_account_element.append({
			"user_id": single_element["user__id"],
			"thumbnail_image_url": settings.MEDIA_URL + single_element["image__thumbnail_image__image"],
			"photo_contest_code": photo_contest_code,
		}),

        # user notify section
        if elements_list_type == "notify":
            notify_obj = Notify()
	    user_id = self.request.user.id
	    # retrieve account info
	    user_info = account_obj.get_user_about_id(user_id=user_id)
	    # retrieve user join date
	    account_creation_date = user_info.account.creation_date

            # tiro fuori filtered_list + 1 e la controllo con filtered_list,
            # se c'è un elemento in più non nascondo il pulsante, altrimenti lo nascondo
            filtered_list = notify_obj.user_notify_list(account_creation_date=account_creation_date, user_id=user_id, filters_list=filters_list)
            # return a valid filtered list, trick to hide "load more button"
            valid_filtered_list = self.return_valid_filtered_list(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"])

            if valid_filtered_list:
                for notify in valid_filtered_list:
                    # se la notifica è stata creata dopo l'utente allora gliela faccio visualizzare
                    # if notify_obj.check_if_show_notify(user_id=self.request.user.id, notify_date=notify["creation_date"]):
		    json_account_element.append({
			"notify_id": str(notify.notify_id),
			"title": str(notify.title),
			"creation_date": str(formats.date_format(notify.creation_date, "SHORT_DATE_FORMAT")),
			"already_read": str(notify.user_notify_id or ''),
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

        # if exists elements
        if filtered_list:
            logger.debug("len: " + str(len(filtered_list)))
            logger.debug("show limit: " + str(filters_list["elements_per_call"]-1))
            # check if show or hide "load more" button
            if self.check_if_exists_more_elements(filtered_list=filtered_list, show_limit=filters_list["elements_per_call"]):
                show_load_button = True

        data = {'success' : True, 'elements_list_type': elements_list_type, 'elements_list': json_account_element, 'show_load_button': show_load_button,}
        json_data_string = json.dumps(data) # WARNING: se la query non è stata eseguita precedente (tramite list, loop, ecc...) questo fa un botto di chiamate al db inutili
        self.set_json_response(json_response=json_data_string)

        return True

    def perform_voting(self):
        """Function to perform a vote action"""
        logger.debug("ajax_function: @@perform_voting@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        Account_obj = Account()
        CommonUtils_obj = CommonUtils()
        Vote_obj = Vote()
        Contest_obj = Contest()

        from_user_id = self.request.user.id
        to_user_id = self.request.POST.get("user_id")
        vote_code = self.request.POST.get("vote_code")
        error_msg = ""

	# controllo che l'utente votante abbia verificato la mail
        if not Account_obj.has_permission(user_obj=self.request.user, permission_codename='user_verified'):
	    logger.error("perform_voting error, utente non verificato")
            error_msg = "Non è possibile votare se non viene verificato l'account."
        elif not Contest_obj.check_if_account_contest_is_active(user_id=to_user_id):
	    # controllo che il contest sia aperto
            logger.error("perform_voting error, contest non attivo | error code: " + str(ContestNotActiveError.get_error_code))
            error_msg = "Non è possibile votare fino all'apertura del concorso."
        else:
            try:
                # check if user can be voted
                Vote_obj.check_if_user_can_vote(from_user_id=from_user_id, to_user_id=to_user_id, request=self.request)
            except UserAlreadyVotedError:
                logger.error("perform_voting error, utente già votato | error code: " + str(UserAlreadyVotedError.get_error_code))
                error_msg = "Non puoi votare più volte lo stesso utente nell'arco di 7 giorni."
            else:
                try:
                    # try to perform voting
                    Vote_obj.perform_votation(from_user_id=from_user_id, to_user_id=to_user_id, vote_code=vote_code, request=self.request)
                except (PerformVotationDataMissingError, PerformVotationVoteCodeDataError, PerformVotationFromUserMissingError, PerformVotationToUserMissingError, PerformVotationUserContestMissingError):
                    logger.error("errore nella votazione di: " + str(to_user_id) + " da parte di: " + str(from_user_id) + " con vote code: " + str(vote_code))
                    error_msg = "Errore inaspettato nella votazione, per favore riprova più tardi."
                else:
                    # votation successfully performed, attach cookie to response
                    self.cookie_key = project_constants.USER_ALREADY_VOTED_COOKIE_NAME + str(to_user_id)
                    self.cookie_value = True
                    self.cookie_expiring = project_constants.SECONDS_BETWEEN_VOTATION

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
        Account_obj = Account()

        # retrieve uploaded image data
        image_data = {}
        image_data["image_id"] = self.request.POST.get("image_id")
        image_data["image_type"] = self.request.POST.get("image_type")
        image_data["user"] = self.request.user

        # proseguire con i controlli (forse, è tardi per pensarci) -> tempo dopo -> fatto
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
            if image_data["image_type"] == project_constants.IMAGE_TYPE["profile"]:
                # se è stata uploadata l'immagine del profilo, abilito l'utente a sfilare sulla passerella
                Account_obj.set_user_can_be_shown(value=1, user=self.request.user)
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
        user_id = self.request.POST.get("user_id")

        try:
            # retrieve user info
            account_info = account_obj.custom_user_id_data(user_id=user_id)
        except User.DoesNotExist:
            # user id doesn't exists
            data = {'error' : True, 'message': "Controllare i parametri della chiamata"}
            pass
        else:
            # retrieve contest user info
            contest_account_info = account_obj.get_contest_account_info(user_id=user_id, contest_type=account_info["contest_type_code"])
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

    def count_unread_notify(self):
        """Function to count unread notify"""
        logger.debug("ajax_function: @@get_user_info@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        account_obj = Account()
        notify_obj = Notify()

        # current logged user id
        user_id = self.request.user.id

        try:
            # retrieve user info
            account_info = account_obj.custom_user_id_data(user_id=user_id)
        except User.DoesNotExist:
            # user id doesn't exists
            data = {'error' : True, 'message': "Id utente non esistente: " + str(user_id)}
            pass
        else:
            # count unread notify number
            unread_notify_number = notify_obj.count_notify_to_read(user_id=user_id)

            # set cookie to not show user notify popup for next x seconds
            self.cookie_key = project_constants.USER_NOTIFY_POPUP_SHOWN_COOKIE_NAME
            self.cookie_value = True
            self.cookie_expiring = project_constants.USER_NOTIFY_POPUP_SHOWN_COOKIE_EXPIRING_SECONDS

            # build json response
            data = {
                    'success' : True,
                    'unread_notify_total': unread_notify_number,
                    'user_first_name' : account_info["first_name"],
            }

        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def add_photoboard_like(self):
        """Function to add a photoboard like"""
        logger.debug("ajax_function: @@add_photoboard_like@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        # common method class init
        CommonUtils_obj = CommonUtils()
        ImageContestImage_obj = ImageContestImage()
        ImageContestVote_obj = ImageContestVote()

        msg = ""
        error_flag = False
        user_id = self.request.POST.get("user_id")
        image_contest_image_id = self.request.POST.get("image_contest_image_id")
        ip_address = CommonUtils_obj.get_ip_address(request=self.request)

        # check if exists image_contest_image
        try:
            ImageContestVote_obj.perform_votation(image_contest_image_id=image_contest_image_id, ip_address=ip_address, request=self.request)
        except ImageContestImage.DoesNotExist:
            # image_contest_image doesn't exist error
            msg = "Non è stato possibile aggiungere il like (immagine non esistente)."
            error_flag = True
        except ImageContestClosedError:
            # image found but not in current contest
            msg = "Immagine trovata ma non nel contest aperto (immagine fuori dalla votazione)."
        except ImageAlreadyVotedError:
            # image_contest_image already voted error
            msg = "La foto è già stata votata."
            error_flag = True
        else:
            # votation performing seems ok, attach cookie to response
            self.cookie_key = ICA_VATE_COOKIE_NAME + str(image_contest_image_id)
            self.cookie_value = True
            self.cookie_expiring = ICA_VATE_COOKIE_EXPIRING
            pass

        if error_flag:
            data = {'error' : True, 'message': msg}
        else:
            data = {'success' : True, 'message': msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def resend_confirmation_email(self):
        """Function to resend a confirmation email"""
        logger.debug("ajax_function: @@resend_confirmation_email@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        # retrieve account info
        account_obj = Account()
        user_obj = self.request.user
        user_id = user_obj.id
        account_info = account_obj.custom_user_id_data(user_id=user_id)

        # if activation_key is empty then generating a new ones
        if not account_info["activation_key"]:
            account_info["activation_key"] = account_obj.create_auth_token(email=account_info["email"])
            # save activation_key into account object
            save_data = {'activation_key' : account_info["activation_key"]}
            account_obj.update_data(save_data=save_data, user_obj=user_obj)

        # resend confirmation email
        email_context = {
            "first_name": account_info["first_name"],
            "last_name": account_info["last_name"],
            "auth_token": account_info["activation_key"],
        }
        CustomEmailTemplate(
            email_name="user_activate_email",
            email_context=email_context,
            template_type="user",
            recipient_list=[account_info["email"],]
        )

        data = {'success' : True}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def publish_interview(self):
        """Function to publish an user interview"""
        logger.debug("ajax_function: @@publish_interview@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        """
            Se già verificata pubblico direttamente, setto come pubblicata
            altrimenti setto come in fase di analisi e mando una mail ad admin
        """

        account_obj = Account()
        survey_obj = Survey()
        user_survey_obj = UserSurvey()

        msg = ""
        error_flag = False
        user_obj = self.request.user
        user_id = user_obj.id
        survey_code = self.request.POST.get("survey_code")

        # check survey code exists
        if survey_obj.check_survey_code_exists(survey_code=survey_code):
            try:
                # retrieve survey about user_id
                existing_user_survey_obj = user_survey_obj.get_user_survey(survey_code=survey_code, user_id=user_id)
            except UserSurvey.DoesNotExist:
                # errore
                msg = "L'utente " + str(user_id) + " non ha ancora creato un survey."
                logger.error("publish_interview: " + str(msg) + " | request: " + str(self.request))
                error_flag = True
            else:
                if existing_user_survey_obj.is_survey_approved():
                    # user survey can be published
                    existing_user_survey_obj.set_publishing_status(publishing_status=DS_CONST_PUBLISHED)

                    # setto messaggio di pubblicazione (e classe), di approvazione (e classe) e testo del popup
                    publishing_msg = user_survey_obj.get_survey_publishing_label(publishing_status=DS_CONST_PUBLISHED)
                    publishing_class = 'verified_label'
                    approving_msg = user_survey_obj.get_survey_approving_label(approving_status=DS_CONST_APPROVED)
                    approving_class = 'verified_label'
                    popup_msg = "L'intervista è stata pubblicata correttamente sul tuo profilo."
                else:
                    # set approving status
                    existing_user_survey_obj.set_pending_approving_status()

                    # current logged in user info
                    account_info = account_obj.custom_user_id_data(user_id=user_id)

                    # send approve interview email to admin
                    email_context = {
                        "user_id": account_info["user_id"],
                        "first_name": account_info["first_name"],
                        "last_name": account_info["last_name"],
                        "email": account_info["email"],
                        "profile_url": settings.SITE_URL + "/passerella/dettaglio-utente/" + str(account_info["user_id"]) + "/",
                        "confirm_survey_url": settings.SITE_URL + "/admin/verify-interview/" + str(existing_user_survey_obj.user_survey_id) + "/",
                    }

                    CustomEmailTemplate(
                        email_name="approve_interview_email",
                        email_context=email_context,
                        template_type="user",
                    )

                    # setto messaggio di pubblicazione (e classe), di approvazione (e classe) e testo del popup
                    publishing_msg = user_survey_obj.get_survey_publishing_label(publishing_status=DS_CONST_NOT_PUBLISHED)
                    publishing_class = ''
                    approving_msg = user_survey_obj.get_survey_approving_label(approving_status=DS_CONST_PENDING_APPROVAL)
                    approving_class = 'in_progress_label'
                    popup_msg = "Grazie per la partecipazione, l'intervista è in fase di approvazione, verrà pubblicata automaticamente non appena sarà approvata.<br />Rimani in attesa!"

        if error_flag:
            data = {'error' : True, 'msg' : msg}
        else:
            data = {
                'success' : True,
                'msg' : msg,
                'publishing_msg' : publishing_msg,
                'publishing_class' : publishing_class,
                'approving_msg' : approving_msg,
                'approving_class' : approving_class,
                'popup_msg' : popup_msg
            }

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def unpublish_interview(self):
        """Function to unpublish an user interview"""
        logger.debug("ajax_function: @@unpublish_interview@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        account_obj = Account()
        survey_obj = Survey()
        user_survey_obj = UserSurvey()

        msg = ""
        success_flag = False
        user_obj = self.request.user
        user_id = user_obj.id
        survey_code = self.request.POST.get("survey_code")

        # check survey code exists
        if survey_obj.check_survey_code_exists(survey_code=survey_code):
            try:
                # retrieve survey about user_id
                existing_user_survey_obj = user_survey_obj.get_user_survey(survey_code=survey_code, user_id=user_id)
            except UserSurvey.DoesNotExist:
                # errore
                msg = "L'utente " + str(user_id) + " non ha ancora creato un survey."
                logger.error("unpublish_interview: " + str(msg) + " | request: " + str(self.request))
            else:
                # unpublish user interview
                existing_user_survey_obj.set_publishing_status(publishing_status=DS_CONST_NOT_PUBLISHED)
                # retrieve unpublish msg
                unpublishing_msg = user_survey_obj.get_survey_publishing_label(publishing_status=DS_CONST_NOT_PUBLISHED)
                success_flag = True

        if success_flag:
            data = {'success' : True, 'unpublishing_msg' : unpublishing_msg}
        else:
            data = {'error' : True, 'msg' : msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def add_image_to_photocontest(self):
        """Function to add a photo to a photocontest"""
        logger.debug("ajax_function: @@add_image_to_photocontest@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        from django_photo_contest.models import PhotoContest, PhotoContestPictures
        account_obj = Account()
        photo_contest_obj = PhotoContest()
        photo_contest_pictures_obj = PhotoContestPictures()

        msg = ""
        success_flag = False
        user_obj = self.request.user
        user_id = user_obj.id
        book_image_id = self.request.POST.get("book_image_id")
        photocontest_code = self.request.POST.get("photocontest_code")

        #XXX: check futuri, controllare che il 'book_image_id' appartenga effettivamente a questo utente

        # retrieve user info
        account_info = account_obj.custom_user_id_data(user_id=user_id)

        # controllo se l'utente è già presente oppure no all'interno del photocontest
        if not photo_contest_pictures_obj.exists_user_photocontest_picture(user_id=user_id, photocontest_code=photocontest_code):
            try:
                # try to retrieve photocontest obj
                selected_photocontest_obj = photo_contest_obj.get_by_code_contest_type(code=photocontest_code, contest_type_code=account_info["contest_type_code"])
            except PhotoContest.DoesNotExist:
                # nothing photocontest found
                msg = "Nessun photocontest trovato con codice: " + str(photocontest_code) + " e contest_type_code: " + str(account_info["contest_type_code"])
                logger.error("add_image_to_photocontest: " + str(msg) + " | request: " + str(self.request))
                pass
            else:
                # insert photo into photocontest
                photo_contest_pictures_obj.insert_photo_into_contest(user_id=user_id, photo_contest_id=selected_photocontest_obj.photo_contest_id, image_id=book_image_id)
                success_flag = True
        else:
            msg = "User id: " + str(user_id) + " già presente all'interno del photocontest: " + str(photocontest_code)
            logger.error("add_image_to_photocontest: " + str(msg) + " | request: " + str(self.request))

        if success_flag:
            data = {'success' : True}
        else:
            data = {'error' : True, 'msg' : msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def remove_photocontest_image(self):
        """Function to remove a photocontest image"""
        logger.debug("ajax_function: @@remove_photocontest_image@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        from django_photo_contest.models import PhotoContest, PhotoContestPictures
        account_obj = Account()
        photo_contest_obj = PhotoContest()
        photo_contest_pictures_obj = PhotoContestPictures()

        msg = ""
        success_flag = False
        user_obj = self.request.user
        user_id = user_obj.id
        photocontest_code = self.request.POST.get("photocontest_code")

        try:
            # try to delete photocontest image
            photo_contest_pictures_obj.delete_user_photocontest_image(user_id=user_id, photocontest_code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            # no image found on this photocontest
            msg = "Nessun immagine trovata nel photocontest con codice: " + str(photocontest_code)
            logger.error("remove_photocontest_image: " + str(msg) + " | request: " + str(self.request))
            pass
        else:
            # photocontest image successfully deleted
            success_flag = True

        if success_flag:
            data = {'success' : True}
        else:
            data = {'error' : True, 'msg' : msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    def add_photocontest_image_like(self):
        """Function to add photocontest image like"""
        logger.debug("ajax_function: @@add_photocontest_image_like@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))

        from django_photo_contest.models import PhotoContest, PhotoContestPictures, PhotoContestVote, PhotoContestWinner
        import django_photo_contest.settings, django_photo_contest.exceptions
        account_obj = Account()
        photo_contest_obj = PhotoContest()
        photo_contest_pictures_obj = PhotoContestPictures()
        photo_contest_vote_obj = PhotoContestVote()
        photo_contest_winner_obj = PhotoContestWinner()

        msg = ""
        success_flag = False
        user_obj = self.request.user
        user_id = user_obj.id
        photocontest_code = self.request.POST.get("photocontest_code")
        photocontest_user_id = self.request.POST.get("photocontest_user_id")

        try:
            # prelevo le informazioni sulla foto inserita nel photocontest
            user_photocontest_picture_obj = photo_contest_pictures_obj.get_user_photocontest_picture(user_id=photocontest_user_id, photocontest_code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            # ERRORE: la foto da votare non esiste più nel photocontest
            logger.error("foto non più esistente nella votazione di: " + str(photocontest_user_id) + " da parte di: " + str(user_id) + " con photocontest_code: " + str(photocontest_code))
            msg = "Errore inaspettato nella votazione, foto non più esistente, per favore riprova più tardi."
        else:
            if not account_obj.has_permission(user_obj=user_obj, permission_codename='user_verified'):
                # ERRORE: l'utente votante non è stato verificato
                logger.error("add_photocontest_image_like error, utente non verificato")
                msg = "Non è possibile assegnare il like se non viene verificato l'account o non si è registrati."
            elif not photo_contest_vote_obj.check_if_user_can_add_like(user_id=user_id, photo_contest_pictures_id=user_photocontest_picture_obj.photo_contest_pictures_id):
                # ERRORE: utente già votato, il like non può essere assegnato
                logger.error("add_photocontest_image_like error, like già assegnato | error code: " + str(django_photo_contest.exceptions.LikeAlreadyAssigned.get_error_code))
                msg = "Non puoi assegnare il like più volte allo stesso utente nell'arco di 7 giorni."
            else:
                try:
                    # try to add a photocontest image like
                    photo_contest_pictures_obj.add_photocontest_image_like(user_id=photocontest_user_id, photocontest_code=photocontest_code)

                    # prelevo i dati dell'account da votare per creare la votazione
                    account_info = account_obj.custom_user_id_data(user_id=photocontest_user_id)

                    # creo la votazione
                    photo_contest_vote_obj.create_votation(user_id=user_id, photo_contest_pictures_id=user_photocontest_picture_obj.photo_contest_pictures_id, request=self.request)

                    # controllo se per caso l'utente fosse diventato vincitore
                    if photo_contest_pictures_obj.is_photocontest_winner(user_id=photocontest_user_id, photocontest_code=photocontest_code, contest_type_code=account_info.get("contest_type")):
                        # la foto è la vincitrice del photocontest, eseguo le operazioni necessarie
                        photo_contest_winner_obj.manage_photocontest_winner(user_id=photocontest_user_id, photocontest_code=photocontest_code, contest_type_code=account_info.get("contest_type"))
                except PhotoContest.DoesNotExist:
                    # ERRORE: il photocontest non esiste
                    logger.error("utente da votare non più esistente vote_user_id: " + str(photocontest_user_id) + " da parte di: " + str(user_id) + " con photocontest_code: " + str(photocontest_code))
                    msg = "Errore inaspettato nella votazione, photocontest non più esistente."
                except PhotoContestPictures.DoesNotExist:
                    # ERRORE: la foto da votare non esiste più nel photocontest
                    logger.error("foto non più esistente nella votazione di: " + str(photocontest_user_id) + " da parte di: " + str(user_id) + " con photocontest_code: " + str(photocontest_code))
                    msg = "Errore inaspettato nella votazione, foto non più esistente, per favore riprova più tardi."
                except User.DoesNotExist:
                    # ERRORE: l'utente da votare non è più esistente
                    logger.error("utente da votare non più esistente vote_user_id: " + str(photocontest_user_id) + " da parte di: " + str(user_id) + " con photocontest_code: " + str(photocontest_code))
                    msg = "Errore inaspettato nella votazione, utente non più esistente."
                else:
                    # tutto ha funzionato a meraviglia
                    success_flag = True

        if success_flag:
            data = {'success' : True}
        else:
            data = {'error' : True, 'msg' : msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True
