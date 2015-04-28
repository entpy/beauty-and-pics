# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from upload_image_box.models import cropUploadedImages 
from website.exceptions import *
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Book(models.Model):
    # book_id = models.IntegerField(primary_key=True)
    image_id = models.OneToOneField(cropUploadedImages, primary_key=True)
    user = models.ForeignKey(User)
    image_type = models.CharField(max_length=100)

    class Meta:
        app_label = 'account_app'

    def __unicode__(self):
        return self.image_id.url

    # TODO: save an uploaded image:
    #       - se questo image_id non è associato ancora a nessun utente lo
    #       salvo, altrimenti il dato è stato modificato da terzi e lo scarto
    #       (non faccio nessun inserimento)
    #       - return saved image url
    def save_book_image(self, image_data):
        """Function to save a new image (profile image or book image)"""
        return_var = None
        if image_data:
	    try:
                book_obj = Book()
                book_obj.image_id = self.get_crop_uploaded_image_obj(image_id=image_data["image_id"])
	    except croppedImageDoesNotExistError:
	        raise
            else:
                book_obj.user = image_data["user"]
                book_obj.image_type = image_data["image_type"]
                book_obj.save()
                return_var = book_obj.image_id.image.url

        return return_var

    def get_crop_uploaded_image_obj(self, image_id):
        """Function to retrieve crop uploaded image instance"""
        return_var = None
	try:
	    return_var = cropUploadedImages.objects.get(pk=image_id)
            logger.debug("cropped img: " + str(return_var))
	except cropUploadedImages.DoesNotExist:
            raise croppedImageDoesNotExistError

        return return_var

    def check_image_type_exists(self, image_type):
        """Function to check if an image type exists"""
	if image_type not in ['profile_image', 'book_image']:
	    raise imageTypeWrongError

        return True

    def get_photobook_list(self, user_id, filters_list=None):
        """Function to retrieve a list of photobook about a user"""
        return_var = False
        if user_id:
            return_var = Book.objects.values('image_id__id', 'image_id__image').filter(user__id=user_id, image_type=project_constants.IMAGE_TYPE["book"])
            # list orders
            return_var = return_var.order_by('-image_id__id')
            # list limits
            return_var = return_var[filters_list["start_limit"]:filters_list["show_limit"]]

        return return_var

    # TODO
    def get_profile_image(self, user_id):
        """Function to retrieve profile image"""
        return True

"""
	* id_image (PK)
	* user (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""
