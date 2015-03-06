# -*- coding: utf-8 -*-

from django.db import models
from datetime import date
import sys, logging

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger('django.request')

class Account(models.Model):
    id_account = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100)
    status = models.IntegerField(null=True)
    birthday_date = models.DateField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'account_app'

    def check_if_email_exists(self, email_to_check=None):
        """Function to check if an email already exists"""
	return_var = None
	try:
	    Account.objects.get(email=email_to_check)
	    return_var = True
	except Account.DoesNotExist:
	    return_var = False

	return return_var

    def save_data(self, save_data=None):
        """Function to save data inside db"""
	return_var = False
	account_obj = Account()

	# if exists an id_account trying to retrieve modify data about an existing account
	if save_data.get("id_account", 0):
	    try:
	        account_obj = Account.objects.get(id_account=save_data["id_account"])
	    except Account.DoesNotExist:
	        pass

	if "first_name" in save_data:
	    account_obj.first_name = save_data["first_name"]
	if "last_name" in save_data:
	    account_obj.last_name = save_data["last_name"]
	if "email" in save_data:
	    account_obj.email = save_data["email"]
	if "password" in save_data:
	    account_obj.password = save_data["password"]
	if "city" in save_data:
	    account_obj.city = save_data["city"]
	if "country" in save_data:
	    account_obj.country = save_data["country"]
	if "gender" in save_data:
	    account_obj.gender = save_data["gender"]
	if "status" in save_data:
	    account_obj.status = save_data["status"]
	if "birthday_date" in save_data:
	    account_obj.birthday_date = save_data["birthday_date"]

        return_var = account_obj.save()
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

"""
	* id_account (PK)
	* first_name
	* last_name
	* email
	* password
	* city
	* country
	* gender
	* status
	* birthday_date
	* creation_date
	* update_date
"""
