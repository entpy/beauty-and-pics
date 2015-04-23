# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from upload_image_box.models import cropUploadedImages 

class Book(cropUploadedImages):
    book_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    image_id = models.OneToOneField(cropUploadedImages, null=True)

    class Meta:
        app_label = 'account_app'

"""
	* id_image (PK)
	* user (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""

