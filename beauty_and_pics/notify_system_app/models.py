# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import *
from website.exceptions import *
from beauty_and_pics.consts import project_constants
from email_template.email.email_template import *
from account_app.models.accounts import Account
from ckeditor.fields import RichTextField
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Notify(models.Model):

    notify_id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    message = RichTextField()
    action_title = models.CharField(max_length=40, null=True, blank=True)
    action_url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.notify_id) + ' ' + str(self.title)

    def create_notify(self, data):
        """Function to create a notify"""
        return_var = False

        if data.get("title") and data.get("message"):
            notify_obj = Notify()
            notify_obj.title = data.get("title")
            notify_obj.message = data.get("message")
            notify_obj.action_title = data.get("action_title")
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
		# retrieve notify instance
		notify_instance = notify_obj.get_notify_instance(notify_id=kwargs.get('notify_id'))
                # prelevo i dati della notifica per precompilarla nel form
                notify_retrieved = notify_obj.get_notify_info(notify_instance=notify_instance)
        except ValueError:
            pass

	return_var = {
	    "title": request.POST.get('title', notify_retrieved.get('title')),
	    "message": request.POST.get('message', notify_retrieved.get('message')),
	    "action_title": request.POST.get('action_title', notify_retrieved.get('action_title')),
	    "action_url": request.POST.get('action_url', notify_retrieved.get('action_url')),
	}

        return return_var


    def send_notify_via_mail(self, notify_data, recipients_list = []):
        """function to send a custom notify to a recipents list"""
        email_context = {
            "title" : str(notify_data.get('title')),
            "message" : str(notify_data.get('message')),
            "action_title": str(notify_data.get('action_title')),
            "action_url": str(notify_data.get('action_url')),
        }

        # send notify email with custom email template object app ;)
        CustomEmailTemplate(
            email_name="custom_notify_email",
            email_context=email_context,
            template_type="user",
            recipient_list=recipients_list
        )

        return True

    def create_recipients_list(self, retrieve_all_users = False, campaign_contacts_list = [], addictional_email_string = ''):
        """Function to create a recipients list"""
        return_var = []
        addictional_email_list = []

        # all users email
        if retrieve_all_users:
            all_contacts_list = Account.objects.values('user__email').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME)
	    for single_contact in all_contacts_list:
		campaign_contacts_list.append(single_contact['user__email'])

        # retrieve addictional email recipients
        if addictional_email_string:
            for element in addictional_email_string.split(';'):
                addictional_email_list.append(element)

        # concat selected emails with addictional emails
        return_var = campaign_contacts_list + addictional_email_list

        return return_var

    def get_notify_instance(self, notify_id):
        """Function to retrieve notify instance"""
        return_var = None
 
        try:
            return_var = Notify.objects.get(pk=notify_id)
        except Notify.DoesNotExist:
            pass

        return return_var

    def get_notify_info(self, notify_instance):
        """Function to retrieve info (title, description, ecc...) about a notify id"""
        return_var = {}

        return_var['notify_id'] = notify_instance.notify_id
        return_var['creation_date'] = notify_instance.creation_date
        return_var['title'] = notify_instance.title
        return_var['message'] = notify_instance.message
        return_var['action_title'] = notify_instance.action_title
        return_var['action_url'] = notify_instance.action_url

        return return_var

    def count_notify_to_read(self, user_id):
        """Function to count notify not read about a user"""
        return_var = 0
        # total notify number
        total_notify_number = self.count_valid_notify(user_id=user_id)
        # read notify about this user
        total_read_notify = User_Notify.objects.filter(user__id=user_id, notify__creation_date__gte=F('user__account__creation_date')).count()

        if total_notify_number:
            return_var = total_notify_number - total_read_notify

        return return_var

    def count_valid_notify(self, user_id):
        """Function to count total valid notify for user_id"""
        return_var = 0
        account_obj = Account()

        # retrieve account info
        user_info = account_obj.get_user_about_id(user_id=user_id)
        # retrieve user join date
        account_creation_date = user_info.account.creation_date
        # total notify number
        return_var = Notify.objects.filter(Q(creation_date__gte=account_creation_date)).count()

        return return_var

    def exist_valid_notify(self, user_id):
        """Function to check if exist valid notify"""
        return_var = False

        if self.count_valid_notify(user_id=user_id) > 0:
            return_var = True

        return return_var

    def mark_notify_as_read(self, notify_instance, user_instance):
        """Function to mark a notify as read, only if not already exists"""

        return_var = False

        try:
            User_Notify.objects.get(notify=notify_instance, user=user_instance)
        except User_Notify.DoesNotExist:
            user_notify_obj = User_Notify()
            user_notify_obj.user = user_instance
            user_notify_obj.notify = notify_instance
            user_notify_obj.save()
            return_var = True

        return return_var

    def user_notify_list(self, account_creation_date, user_id, filters_list=None):
        """Function to retrieve a list of valid notify about a user"""

	raw_sql = """
	SELECT
	    "notify_system_app_notify"."notify_id",
	    "notify_system_app_notify"."creation_date",
	    "notify_system_app_notify"."title",
	    "notify_system_app_notify"."message",
	    "notify_system_app_notify"."action_title",
	    "notify_system_app_notify"."action_url",
	    "notify_system_app_user_notify"."user_notify_id"
	FROM "notify_system_app_notify" 
	LEFT JOIN "notify_system_app_user_notify" ON ( "notify_system_app_notify"."notify_id" = "notify_system_app_user_notify"."notify_id" ) AND "notify_system_app_user_notify"."user_id" = %(user_id)s 
	WHERE "notify_system_app_notify"."creation_date" >= %(account_creation_date)s
	ORDER BY "notify_system_app_notify"."notify_id" DESC
	"""

	# con le query raw gli slice non vengono aplicati a livello di db, quindi 
	# tramite limit e offset ma a livello di python, quindi se non sono int viene
	# ritornato un errore, questo spiega il comportamento diverso da questa lista
	# a quella dei catwalker, per far funzionare questa query correttamente
	# sono state concatenate la "limit" e la "offset"
        if filters_list.get("start_limit") and filters_list.get("show_limit"):
	    raw_sql += " LIMIT %(show_limit)s OFFSET %(start_limit)s"

	return_var = Notify.objects.raw(raw_sql, {
	    "user_id": user_id, 
	    "account_creation_date": account_creation_date,
	    "start_limit": filters_list.get("start_limit"),
	    "show_limit": filters_list.get("show_limit"),
	})

	# performing query
        return_var = list(return_var)

        return return_var

    def check_if_show_notify(self, user_id, notify_date):
        """Check if a notify could be shown -> (notify_date >= user_creation_date)"""
        return_var = False
        account_obj = Account()

        # retrieve account info
        user_info = account_obj.get_user_about_id(user_id=user_id)
        # retrieve user join date
        account_creation_date = user_info.account.creation_date

        # log some fucking stuff
        logger.info("data creazione account (id=" + str(user_id) + "): " + str(account_creation_date))
        logger.info("data creazione notifica: " + str(notify_date))

        # diff_between_dates = relativedelta(account_creation_date, notify_date)
        if notify_date >= account_creation_date:
            # la notifica è più recente o uguale all'account
            return_var = True
        else:
            # l'account creato è più recente della notifica
            pass

        return return_var

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
