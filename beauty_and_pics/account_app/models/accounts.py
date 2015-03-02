from django.db import models

class Account(models.Model):
    id_account = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    status = models.IntegerField()
    creation_date = models.DateField()
    update_date = models.DateField()

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
	* creation_date
	* update_date
"""
