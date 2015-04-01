# -*- coding: utf-8 -*-

from django.db import models
from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from contest_app.models.contest_types import Contest_Type
from website.exceptions import *
from beauty_and_pics.consts import project_constants
import sys, logging, base64, hashlib, string, random

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

# extends User model
class Account(models.Model):
    # id_account = models.AutoField(primary_key=True)
    # Links Account to a User model instance.
    user = models.OneToOneField(User, primary_key=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)
    birthday_date = models.DateField(null=True)
    hair = models.CharField(max_length=15, null=True) 
    eyes = models.CharField(max_length=15, null=True)
    height = models.CharField(max_length=4, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'account_app'

    def __unicode__(self):
        return self.user.username

    def check_if_email_exists(self, email_to_check=None):
        """Function to check if an email already exists"""
	return_var = None
	try:
	    User.objects.get(email=email_to_check)
	    return_var = True
	except User.DoesNotExist:
	    return_var = False

	return return_var

    def get_user_about_email(self, email=None):
        """Function to retrieve user about an email"""
	return_var = None
	try:
	    return_var = User.objects.get(email=email)
	except User.DoesNotExist:
	    return_var = False
            raise

	return return_var

    def get_user_about_id(self, user_id=None):
        """Function to retrieve user about id"""
	return_var = None
	try:
	    return_var = User.objects.get(pk=user_id)
	except User.DoesNotExist:
	    return_var = False
            raise

	return return_var

    def register_account(self, user_info=None):
        """Function to register a new account"""

        return_var = False
        if user_info:
            account_obj = Account()
            # create new account
            new_user = account_obj.create_user_account(email=user_info["email"], password=user_info["password"])

            # insert addictional data inside User and Account models
            account_obj.update_data(save_data=user_info, user_obj=new_user)
            return_var = True

        return return_var

    def create_user_account(self, email=None, password=None):
        """Function to create user and related account"""
	return_var = False
	account_obj = Account()
        if email and password:
            if not self.check_if_email_exists(email_to_check=email):
                account_obj.user = User.objects.create_user(username=self.__email_to_username(email), email=email, password=password)
                # add "catwalk_user" group in user groups
                account_obj.user.groups.add(self.__create_defaul_user_group())
                account_obj.save()
                return_var = account_obj.user

                # raise an exception if occur errors in account creation
                if not return_var:
                    raise UserCreateError

        return return_var

    def __create_defaul_user_group(self):
        """Function to [create if not exists and] retrieve catwalk_user group"""
        return_var = None
	try:
	    return_var = Group.objects.get(name=project_constants.CATWALK_GROUP_NAME)
	except Group.DoesNotExist:
            # group must be created
            group = Group(name=project_constants.CATWALK_GROUP_NAME)
            group.save()
            return_var = group

        return return_var

    def __email_to_username(self, email):
        """
        Function to convert email to username
        taken from -> https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
        """
        # Emails should be case-insensitive unique
        email = email.lower()
        # Deal with internationalized email addresses
        converted = email.encode('utf8', 'ignore')
        return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]

    # TODO: try to manually raise error in this function
    def update_email_password(self, current_email=None, new_email=None, password=None):
        """Function to update email and password about a user"""
        return_var = False
        if current_email:
            try:
                user_obj = User.objects.get(email=current_email)
            except User.DoesNotExist:
                # send exception to parent try-except block
                raise
            else:
                # save new password
                if password:
                    user_obj.set_password(password)
                # save new email
                if new_email:
                    user_obj.email = new_email
                    # create new username starting from email
                    user_obj.username = self.__email_to_username(email=new_email)
                # save account instance
                if password or new_email:
                    user_obj.save()
                return_var = True

        if not return_var:
            raise UserEmailPasswordUpdateError

        return return_var

    def update_data(self, save_data=None, user_obj=None):
        """Function to save data inside db"""
	return_var = False

        if save_data and user_obj:
            # save User model addictional informations
            if "first_name" in save_data:
                user_obj.first_name = save_data["first_name"]
            if "last_name" in save_data:
                user_obj.last_name = save_data["last_name"]
            # save Account model addictional informations
            if "city" in save_data:
                user_obj.account.city = save_data["city"]
            if "country" in save_data:
                user_obj.account.country = save_data["country"]
            if "gender" in save_data:
                user_obj.account.gender = save_data["gender"]
            if "status" in save_data:
                user_obj.account.status = save_data["status"]
            if "birthday_date" in save_data:
                user_obj.account.birthday_date = save_data["birthday_date"]
            if "hair" in save_data:
                user_obj.account.hair = save_data["hair"]
            if "eyes" in save_data:
                user_obj.account.eyes = save_data["eyes"]
            if "height" in save_data:
                user_obj.account.height = save_data["height"]
            # saving addictiona models data
            user_obj.save()
            user_obj.account.save()
            return_var = user_obj

        if not return_var:
            raise UserUpdateDataError

	return return_var

    def create_date(self, date_dictionary=None, get_isoformat=False):
        """Function to create birthday date starting from dd, mm, yyyy"""
	return_var = False

        if date_dictionary:
            day = date_dictionary.get("day")
            month = date_dictionary.get("month")
            year = date_dictionary.get("year")

            # building birthday date
	    if (day and month and year):
                if get_isoformat:
                    return_var = date(year=int(year), month=int(month), day=int(day)).isoformat()
                else:
                    return_var = date(year=int(year), month=int(month), day=int(day))

        return return_var

    def create_login_session(self, email=None, password=None, request=None):
        """Function to create a login session (logging user inside website)"""
	return_var = False

        if (email and password and request):
            # Use custom email-password backend to check if the email/password
            # combination is valid - a User object is returned if it is.
            user_obj = authenticate(email=email, password=password)

            # If we have a User object, the email and password are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user_obj:
                # Is the account active? It could have been disabled.
                if user_obj.is_active:
                    # If the account is valid and active, we can log the user in.
                    login(request, user_obj)
                    return_var = True
                else:
                    # An inactive account was used - no logging in!
                    raise UserNotActiveError
            else:
                # Ops...email or password not valid - no logging in!
                raise UserLoginError

        return return_var

    def generate_new_password(self):
        """Function to generate a new password"""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def check_user_password(self, request=None, password_to_check=None):
        """Function to check if a password match the current logged in user password"""
        return_var = False
        if request and password_to_check:
            # to see how it works see the docs
            if not request.user.check_password(password_to_check):
                raise UserPasswordMatchError
            return_var = True

        return return_var

    def get_autenticated_user_email(self, request=None):
        """Function to retrieve the email address about current logged in user"""
        return_var = False
        if request and request.user.is_authenticated():
	    return_var = request.user.email
	    logger.info("email of current logged in user: " + str(return_var))

        return return_var

    def get_autenticated_user_data(self, request=None):
        """
        Function to retrieve current user/account logged in data (es. first_name, last_name, gender, ecc...)
        """
        return_var = {}

        if request and request.user.is_authenticated():
            return_var = self.put_user_data_obj_into_dictionary(user_obj=request.user)
	    # logger.info("data about current logged in user: " + str(return_var))

        return return_var

    def custom_user_id_data(self, user_id=None):
        """Function to retrieve user/account info about user id"""
        return_var = {}
        if user_id:
            return_var = self.put_user_data_obj_into_dictionary(user_obj=self.get_user_about_id(user_id=user_id))

        return return_var

    def put_user_data_obj_into_dictionary(self, user_obj=None):
        """Function to convert a user object into dictionary"""
        return_var = {}
        if user_obj:
            # from user model {{{
            return_var["user_id"] = user_obj.id or ''
            return_var["first_name"] = user_obj.first_name or ''
            return_var["last_name"] = user_obj.last_name or ''
            return_var["email"] = user_obj.email or ''
            # from user model }}}
            # from account model {{{
            return_var["city"] = user_obj.account.city or ''
            return_var["country"] = user_obj.account.country or ''
            return_var["gender"] = user_obj.account.gender or ''
            return_var["birthday_date"] = user_obj.account.birthday_date or ''
            return_var["birthday_day"] = str(user_obj.account.birthday_date.day or '')
            return_var["birthday_month"] = str(user_obj.account.birthday_date.month or '')
            return_var["birthday_year"] = str(user_obj.account.birthday_date.year or '')
            return_var["hair"] = user_obj.account.hair or ''
            return_var["eyes"] = user_obj.account.eyes or ''
            return_var["height"] = user_obj.account.height or ''
            # from account model }}}

        return return_var

    # TODO: implement this function
    def get_filtered_accounts_list(self, filters_list=None):
        """Function to retrieve a list of filtere accounts"""
        return_var = False
	# logger.debug("NOME FILTRO: " + str(filters_list["filter_name"]))

	# filter only catwalker users
        return_var = Account.objects.filter(user__groups__name=project_constants.CATWALK_GROUP_NAME)

	# order by "latest_registered" filter
	if filters_list["filter_name"] == "latest_registered":
        	return_var = return_var.order_by('-user__account__creation_date')

	# limits filter
	logger.debug("limite da: " + str(filters_list["start_limit"]))
	logger.debug("limite numero elementi: " + str(filters_list["show_limit"]))
	return_var = return_var[filters_list["start_limit"]:filters_list["show_limit"]]

	logger.debug("@@@: " + str(return_var))

        return return_var
