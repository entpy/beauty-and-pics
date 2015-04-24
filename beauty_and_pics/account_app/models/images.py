# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from upload_image_box.models import cropUploadedImages 
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Book(cropUploadedImages):
    # book_id = models.IntegerField(primary_key=True)
    image_id = models.OneToOneField(cropUploadedImages, primary_key=True)
    user = models.ForeignKey(User)
    image_type = models.CharField(max_length=100)

    class Meta:
        app_label = 'account_app'

    # TODO: save an uploaded image:
    #       - se questo image_id non è associato ancora a nessun utente lo
    #       salvo, altrimenti il dato è stato modificato da terzi e lo scarto
    #       (non faccio nessun inserimento)
    #       - return saved image url
    def save_book_image(self, image_data):
        """Function to save a new image (profile image or book image)"""
        return_var = None
        if image_data:
            book_obj = Book()
            book_obj.image_id = self.get_crop_uploaded_image_obj(image_id=image_data["image_id"])
            book_obj.user = image_data["user"]
            book_obj.image_type = image_data["image_type"]
            book_obj.save()
            return_var = book_obj.image_id.image.url

        return return_var

    def get_crop_uploaded_image_obj(self, image_id):
        """Function to retrieve crop uploaded image instance"""
        return_var = None
	try:
            # TODO: sembra che cancelli la riga
	    return_var = cropUploadedImages.objects.get(pk=image_id)
            #logger.debug("cropped img: " + str(return_var))
	except cropUploadedImages.DoesNotExist:
            raise

        return return_var

"""
	* id_image (PK)
	* user (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""
