from django.db import models

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
