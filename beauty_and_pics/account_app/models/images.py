from django.db import models

class Image(models.Model):
    id_image = models.IntegerField(primary_key=True)
    id_account = models.ForeignKey('Account')
    image_url = models.ImageField(upload_to='book_img/')
    image_type = models.IntegerField()

    class Meta:
        app_label = 'account_app' 

"""
	* id_image (PK)
	* id_account (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""
