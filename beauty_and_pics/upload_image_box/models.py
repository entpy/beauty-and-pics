# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from .settings import *
from PIL import Image
import os, logging, shutil, uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_image_path(self, filename):
    return os.path.join(self.upload_to_base_path, self.upload_to, filename)

class cropUploadedImages(models.Model):
    image = models.ImageField(max_length=500, upload_to=get_image_path)

    upload_to_base_path = APP_BASE_DIRECTORY # default file upload base dir
    upload_to = '' # default file upload custom dir TODO: forse questo non serve

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
            crop_info["custom_crop_dir_name"] = request.POST.get("custom_crop_dir_name") + "/"

	    """
	    logger.debug("=== crop info START ===")
	    logger.debug("file_id: " + str(crop_info["file_id"]))
	    logger.debug("height: " + str(crop_info["height"]))
	    logger.debug("width: " + str(crop_info["width"]))
	    logger.debug("x: " + str(crop_info["x"]))
	    logger.debug("y: " + str(crop_info["y"]))
	    logger.debug("rotate" + str(crop_info["rotate"]))
	    logger.debug("custom_crop_dir_name" + str(crop_info["custom_crop_dir_name"]))
	    logger.debug("=== crop info END ===")
	    """

	return crop_info

    def get_crop_box(self, crop_info):
	"""Function to retrieve a crop box"""
	return_var = False
	if crop_info:
	    return_var = (crop_info["x"], crop_info["y"], crop_info["x"]+crop_info["width"], crop_info["y"]+crop_info["height"])

        return return_var

    def crop_image(self, uploaded_image, crop_info, custom_crop_directory_name=None):
        """Function to crop an image"""
	return_var = False
	if uploaded_image and crop_info:
            uploaded_image_path = str(uploaded_image.image.path)
            image = Image.open(uploaded_image_path)
            cropped_image = image.crop(self.get_crop_box(crop_info))
            cropped_width, cropped_height = cropped_image.size   # get dimensions about cropped image
            if cropped_width >= CROPPED_IMG_MIN_WIDTH and cropped_height >= CROPPED_IMG_MIN_HEIGHT:
		# TODO: move image to another directory (custom directory)
		self.move_cropped_image(uploaded_image, cropped_image, custom_crop_directory_name)
	        return_var = True

        return return_var

    def move_cropped_image(self, uploaded_image, cropped_image, custom_crop_directory_name=None):
        """Function to save cropped image into CROPPED_IMG_DIRECTORY directory"""
	tmp_uploaded_image_full_path = uploaded_image.image.path
	# retrieve image name from tmp_uploaded_image_full_path
	tmp_uploaded_image_name = self.get_image_name(tmp_uploaded_image_full_path)
	# retrieve crop image directory
	crop_image_directory = self.get_crop_image_directory(custom_crop_directory_name)
	# build crop image full path (crop_image_directory + tmp_uploaded_image_name)
	crop_image_full_path = crop_image_directory + tmp_uploaded_image_name

	# debug info
        logger.debug("tmp_uploaded_image_full_path: " + str(tmp_uploaded_image_full_path))
        logger.debug("crop_image_full_path: " + str(crop_image_full_path))

	# create cropped image directory if not exists
	self.create_cropped_image_directory(crop_image_directory)
	# copy tmp uploaded file into new position
	shutil.copy2(tmp_uploaded_image_full_path, crop_image_full_path)
	# crop file moved into new position
	cropped_image.save(crop_image_full_path)

	# save cropped image info into database
	self.save_image_info(APP_BASE_DIRECTORY + CROPPED_IMG_DIRECTORY + self.get_custom_crop_directory(custom_crop_directory_name) + tmp_uploaded_image_name)

	return True

    def create_cropped_image_directory(self, directory):
        """Function to create crop image directory if not exists"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_image_name(self, full_image_path):
	"""Function to retrieve image name about a full image path like this: '/tmp/image/file1.png' -> must return 'file1.png' """
	head, tail = os.path.split(full_image_path)
	file_name, file_extension = os.path.splitext(full_image_path)
	# low risk of file name collision (if file exists generate a new name)
	new_file_name = str(uuid.uuid4()) + file_extension

	return new_file_name

    def get_crop_image_directory(self, custom_crop_directory_name=None):
	"""Function to build crop image directory"""
	crop_image_directory = settings.MEDIA_ROOT + "/" + APP_BASE_DIRECTORY + CROPPED_IMG_DIRECTORY + self.get_custom_crop_directory(custom_crop_directory_name)
        logger.debug("crop_image_directory: " + str(crop_image_directory))

	return crop_image_directory

    def get_custom_crop_directory(self, custom_crop_directory_name=None):
	"""Function to retrieve default custom crop directory name"""
	return_var = False
	if custom_crop_directory_name:
	    return_var = custom_crop_directory_name
	else:
	    return_var = CUSTOM_CROPPED_IMG_DIRECTORY

	return return_var

    def save_image_info(self, image_url):
	"""Function to save image into database"""
        crop_uploaded_images_obj = cropUploadedImages()
        crop_uploaded_images_obj.image = image_url
	crop_uploaded_images_obj.save()

	return True

    def custom_crop_directory_valid(self, request, custom_directory_name):
	"""Function to check if a custom crop directory is valid"""
	return_var = False
	logger.debug("valore in sessione: " + str(request.session.get('directory_name', False)))
	if request.session['CUSTOM_CROPPED_IMG_DIRECTORY'] == custom_directory_name:
	    return_var = True

	return return_var

class tmpUploadedImages(models.Model):
    image = models.ImageField(max_length=500, upload_to=get_image_path)
    upload_date = models.DateTimeField(auto_now=True)

    # upload file attributes
    upload_to_base_path = APP_BASE_DIRECTORY # default file upload base dir
    upload_to = '' # default file upload custom dir TODO: forse questo non serve

    def __unicode__(self):
        return self.image

    # TODO
    def delete_tmp_images(self):
        """Function to delete old tmp uploaded images"""
	return True
