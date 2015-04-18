# -*- coding: utf-8 -*-

from django.db import models
from .settings import *
from PIL import Image
import os

def get_image_path(self, filename):
    return os.path.join(self.upload_to_base_path, self.upload_to, filename)

class uploadedImages(models.Model):
    image = models.ImageField(max_length=500, upload_to=get_image_path)
    upload_date = models.DateTimeField(auto_now=True)
    is_temp_image = models.IntegerField(null=True, default=1)

    # upload file attributes
    upload_to_base_path = APP_BASE_DIRECTORY # default file upload base dir
    upload_to = '' # default file upload custom dir

    def __unicode__(self):
        return self.image

    def retrieve_crop_info(self, request):
        """Function to retrieve info about javascript crop plugin"""
        crop_info = {}

	if request:
            crop_info["file_id"] = request.POST.get("file_id") # BAD
            crop_info["height"] = int(float(request.POST.get("height")))
            crop_info["width"] = int(float(request.POST.get("width")))
            crop_info["x"] = int(float(request.POST.get("x")))
            crop_info["y"] = int(float(request.POST.get("y")))
            crop_info["rotate"] = request.POST.get("rotate")
	    """
	    logger.debug("=== crop info START ===")
	    logger.debug("file_id: " + str(crop_info["file_id"]))
	    logger.debug("height: " + str(crop_info["height"]))
	    logger.debug("width: " + str(crop_info["width"]))
	    logger.debug("x: " + str(crop_info["x"]))
	    logger.debug("y: " + str(crop_info["y"]))
	    logger.debug("rotate" + str(crop_info["rotate"]))
	    logger.debug("=== crop info END ===")
	    """

	return crop_info

    def get_crop_box(self, crop_info):
	"""Function to retrieve a crop box"""
	return_var = False
	if crop_info:
	    return_var = (crop_info["x"], crop_info["y"], crop_info["x"]+crop_info["width"], crop_info["y"]+crop_info["height"])

        return return_var

    def crop_image(self, uploaded_image, crop_info):
        """Function to crop an image"""
	return_var = False
	if uploaded_image and crop_info:
            uploaded_image_path = str(uploaded_image.image.path)
            image = Image.open(uploaded_image_path)
            cropped_image = image.crop(self.get_crop_box(crop_info))
            cropped_width, cropped_height = cropped_image.size   # get dimensions about cropped image
            if cropped_width >= CROPPED_IMG_MIN_WIDTH and cropped_height >= CROPPED_IMG_MIN_HEIGHT:
		# TODO: move image to another directory (custom directory)
	        cropped_image.save(uploaded_image_path)
	        return_var = True

        return return_var
