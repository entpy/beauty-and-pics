# -*- coding: utf-8 -*-

from django.db import models
from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from website.exceptions import *
import sys, logging, base64, hashlib, string, random

# force utf8 read data
reload(sys);
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
                account_obj.user = User.objects.create_user(username=self._email_to_username(email), email=email, password=password)
                account_obj.save()
                return_var = account_obj.user

                # raise an exception if occur errors in account creation
                if not return_var:
                    raise UserCreateError

        return return_var

    def _email_to_username(self, email):
        """
        Function to convert email to username
        taken from -> https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
        """
        # Emails should be case-insensitive unique
        email = email.lower()
        # Deal with internationalized email addresses
        converted = email.encode('utf8', 'ignore')
        return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]

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

    def update_user_password(self, email=None, new_password=None):
        """Function to replace user password with new generated password (used in recovery password)"""
        return_var = False
        if email and new_password:
	    try:
	        u = User.objects.get(email=email)
	    except User.DoesNotExist:
	        logger.error("recupero password per un utente non esistente: email=" + str(email))
                raise User.DoesNotExist
            else:
	        u.set_password(new_password)
	        u.save()
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
            # from user model {{{
	    return_var["first_name"] = request.user.first_name or ''
	    return_var["last_name"] = request.user.last_name or ''
	    return_var["email"] = request.user.email or ''
            # from user model }}}
            # from account model {{{
	    return_var["city"] = request.user.account.city or ''
	    return_var["country"] = request.user.account.country or ''
	    return_var["gender"] = request.user.account.gender or ''
	    return_var["birthday_date"] = request.user.account.birthday_date or ''
	    return_var["birthday_day"] = str(request.user.account.birthday_date.day or '')
	    return_var["birthday_month"] = str(request.user.account.birthday_date.month or '')
	    return_var["birthday_year"] = str(request.user.account.birthday_date.year or '')
	    return_var["hair"] = request.user.account.hair or ''
	    return_var["eyes"] = request.user.account.eyes or ''
	    return_var["height"] = request.user.account.height or ''
            # from account model }}}

	    logger.info("data about current logged in user: " + str(return_var))

        return return_var
