# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import *
from website.exceptions import *
from beauty_and_pics.consts import project_constants
from email_template.email.email_template import *
from account_app.models.accounts import Account
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Notify(models.Model):

    # notify type selection
    """
    NOTIFY_EMAIL = 1
    NOTIFY_WEBPUSH = 2
    NOTIFY_TYPE = ((NOTIFY_EMAIL, 'Notify via email'), (NOTIFY_WEBPUSH, 'Notify via webpush'),)
    """

    notify_id = models.AutoField(primary_key=True)
    # type = models.IntegerField(choices=NOTIFY_TYPE, default=NOTIFY_WEBPUSH)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    action_url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.notify_id) + ' ' + str(self.title)

    # function to create a notify
    def create_notify(self, data):
        return_var = False

        if data.get("title") and data.get("message"):
            notify_obj = Notify()
            notify_obj.title = data.get("title")
            notify_obj.message = data.get("message")
            notify_obj.action_url = data.get("action_url")
            notify_obj.save()
            return_var.notify_id

        return return_var

    def set_campaign_user(self, senders_dictionary, request):
            """
            Function to set (or unset) accounts to receive a promotion.
            This function works like this:
                { "id_account" : 1 } => to enable
                { "id_account" : 0 } => to disable

            So, for example, if you works with a dictionary like this:
                { "4" : 1, "5" : 1, "6" : 0, "7" : 1, "8" : 0 }
            You can create previously dictionary with "Campaign.get_senders_dictionary()" function.

            Users 4, 5, 7 will be enabled, while users 6, 8 will be disabled.
            Enabled or disable means row added or removed from db with
            "add_campaign_user" or "remove_campaign_user" functions.
            Return True on success
            """

            if not request.session.get('checked_users'):
                request.session['checked_users'] = {}

            if senders_dictionary:
                for key, value in senders_dictionary.iteritems():
                    if value:
                        request.session['checked_users'][str(key)] = 1
                        logger.debug("aggiungo in sessione: " + str(key))
                    else:
                        request.session['checked_users'][str(key)] = 0
                        logger.debug("rimuovo dalla sessione: " + str(key))

            logger.debug("set_campaign_user, checked_users in SESSION: " + str(request.session['checked_users']))
            return request.session['checked_users']

    def get_checkbox_dictionary(self, paginator_element_list=False, checked_elements=False):
            """
            Function to render a senders dictionary like this:
            { "mail1@mail.com" : 1, "mail2@mail.com" : 1, "mail3@mail.com" : 0, "mail4@mail.com" : 1, "mail5@mail.com" : 0 }
            Return a checkbox status dictionary on success

            paginator_element_list: all objects in current view (list)
            checked_elements: all checkbox select in current view (list)
            (string) -> es <input type="checkbox" name="checkbox_name[23]" value="1"> 23 is the unique database model ID, like id_account
            """

            checkbox_dictionary = {}

            for element in paginator_element_list:
                # logger.debug("get_checkbox_dictionary, element: " + str(element.user.id))
                # se element è contenuto in checked_elements allora ok
                if (str(element.user.email) in checked_elements):
                    checkbox_dictionary[element.user.email] = 1
                else:
                    checkbox_dictionary[element.user.email] = 0

            # logger.error("models.py, get_senders_dictionary: " + str(checkbox_dictionary))
            logger.debug("get_checkbox_dictionary, checkbox_dictionary: " + str(checkbox_dictionary))

            return checkbox_dictionary

    def get_account_list(self, request):
            """
            Function to retrieve all checked account from session
            Return an account id list on success
            """

            return_var = []

            if request.session.get('checked_users'):
                for key, value in request.session.get('checked_users').iteritems():
                    if value:
                        logger.debug("[get_account_list], single_elements: key=" + str(key) + " value=" + str(value))
                        return_var.append(str(key))

            return return_var

    def save_checked_elemets(self, paginator, request = {}):
        """Function to save into session checked elements from djago paginator"""
        notify_obj = Notify()
        # previously page number
        old_viewed_page = request.POST.get('current_page', 1)

        # add/remove id into session
        checked_contacts = request.POST.getlist('contacts[]')

        # retrieving checked list from current view (only checkbox that are shown from paginator current view)
        senders_dictionary = notify_obj.get_checkbox_dictionary(paginator.page(old_viewed_page), checked_contacts)

        # saving or removing checked/unchecked checkbox from db
        checked_users = notify_obj.set_campaign_user(senders_dictionary=senders_dictionary, request=request)

        return checked_users

    def build_form_initial_value(self, request, kwargs = {}):
        """Function to build admin form initial value dictionary"""
        notify_obj = Notify()
        notify_retrieved = {}
        try:
            if int(kwargs.get('notify_id') or 0):
                # prelevo i dati della notifica per precompilarla nel form
                notify_retrieved = notify_obj.get_notify_info(notify_id=kwargs.get('notify_id'))
        except ValueError:
            pass

	return_var = {
	    "title": request.POST.get('title', notify_retrieved.get('title')),
	    "message": request.POST.get('message', notify_retrieved.get('message')),
	    "action_url": request.POST.get('action_url', notify_retrieved.get('action_url')),
	}

        return return_var


    def send_notify_via_mail(self, notify_data, recipients_list):
        """function to send a custom notify to a recipents list"""
        email_context = {
            "title" : str(notify_data.get('title')),
            "message" : str(notify_data.get('message')),
            "action_url": str(notify_data.get('action_url')),
        }

        # send notify email with custom email template object app ;)
        CustomEmailTemplate(
            email_name="custom_notify_email",
            email_context=email_context,
            template_type="user",
            recipient_list=[recipients_list,]
        )

        return True

    def create_recipients_list(self, retrieve_all_users = False, campaign_contacts_list = [], addictional_email_string = ''):
        """Function to create a recipients list"""
        return_var = []
        addictional_email_list = []

        # TODO fare qui
        if retrieve_all_users:
            all_contacts_list = Account.objects.values('user__email').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME)

        # retrieve addictional email recipients
        if addictional_email_string:
            for element in addictional_email_string.split(';'):
                addictional_email_list.append(element)

        # concat selected emails with addictional emails
        recipients_list = campaign_contacts_list + addictional_email_list

        return return_var

    # function to mark a notify as read
    def mark_notify_as_read(self, notify_id, user_id):
        return True

    # function to count notify not read about a user
    def count_notify_to_read(self, user_id):
        return True

    # function to retrieve info (title, description, ecc...) about a notify id
    def get_notify_info(self, notify_id):
        return_var = {}

        try:
            notify_obj = Notify.objects.get(pk=notify_id)
        except Notify.DoesNotExist:
            pass
        else:
            return_var['notify_id'] = notify_obj.notify_id
            return_var['creation_date'] = notify_obj.creation_date
            return_var['title'] = notify_obj.title
            return_var['message'] = notify_obj.message
            return_var['action_url'] = notify_obj.action_url

        return return_var

    # function to retrieve a list of notify about a user
    def user_notify_list(self, filters, user_id):
        return True

"""
# la notifica può essere inviata via mail o vista solo sul sito (tipo push)
class Notify_Type(models.Model):
    notify_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.description)
"""

# se è presente una riga qua, la notifica è stata letta dall'utente
# valido solo per le notifiche sul sito
class User_Notify(models.Model):
    user_notify_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    notify = models.ForeignKey(Notify)
    read_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.user_notify_id)
